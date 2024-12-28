from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from db import tools
from schemas.me import UpdatePasswordRequest, UpdateProfileRequest
from utils.jwt import jwt_tools
from utils.utils import collect_user_data, hash_password, validation_user_data

router = APIRouter(prefix="/me", tags=["me"])


@router.get("/profile")
async def profile(current_user=Depends(jwt_tools.get_current_user)):
    user = await tools.get_user(current_user["login"])
    content = collect_user_data(user)

    return JSONResponse(status_code=200, content=content)


@router.patch("/profile")
async def profile(data: UpdateProfileRequest, current_user=Depends(jwt_tools.get_current_user)):
    if not await validation_user_data.validate_update_profile_request(data):
        # TODO: add errorResponse
        return JSONResponse(status_code=400, content={})
    
    # TODO: add 409 error

    user = await tools.update_user(current_user["login"], data.model_dump())
    content = collect_user_data(user)

    return JSONResponse(status_code=200, content=content)


@router.post("/updatePassword")
async def update_password(data: UpdatePasswordRequest, current_user=Depends(jwt_tools.get_current_user)):
    if hash_password(data.oldPassword) != current_user["passwordHash"]:
        # TODO: add errorResponse
        return JSONResponse(status_code=403, content={})

    if not validation_user_data.validate_password(data.newPassword):
        # TODO: add errorResponse
        return JSONResponse(status_code=400, content={})

    await tools.delete_sessions(current_user["id"])
    await tools.update_user(current_user["login"], {"passwordHash": hash_password(data.newPassword)})

    return JSONResponse(status_code=200, content={"status": "ok"})
