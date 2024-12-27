from fastapi import APIRouter
from fastapi.responses import JSONResponse

from db import tools
from schemas.auth import RegisterRequest, SignInRequest
from utils.jwt import jwt_tools
from utils.utils import hash_password, validation_user_data

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(request: RegisterRequest):
    try:
        if not await validation_user_data.vaidate_register_request(request):
            return JSONResponse(status_code=400, content={})
        status, user = await tools.create_user(request.login, request.password, request.email, request.countryCode, request.isPublic, request.image, request.phone)
        if status != 0:
            return JSONResponse(status_code=409, content={})
        return JSONResponse(status_code=201, content=user)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={})


@router.post("/sign-in")
async def sign_in(request: SignInRequest):
    try:
        user, id = await tools.sign_in(request.login, request.password)
        if user:
            token = jwt_tools.encode(
                user["login"],
                id,
                hash_password(user["passwordHash"])
            )

            return JSONResponse(
                status_code=200,
                content={"token": token},
                headers={"Authorization": f"Bearer {token}"}
            )
        return JSONResponse(status_code=401, content={})
    except Exception:
        return JSONResponse(status_code=400, content={})
