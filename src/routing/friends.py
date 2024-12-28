from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from db import tools
from schemas.friends import AddFriendRequest
from utils.jwt import jwt_tools

router = APIRouter(prefix="/friends", tags=["friends"])


@router.post("/add")
async def add_friend(data: AddFriendRequest, current_user=Depends(jwt_tools.get_current_user)):
    status = await tools.add_friend(current_user["id"], data.login)
    if status == 1:
        # TODO: add errorResponse
        return JSONResponse(status_code=404, content={"status": "error", "message": "User not found"})
    return JSONResponse(status_code=200, content={"status": "ok"})


@router.post("/remove")
async def remove_friend(data: AddFriendRequest, current_user=Depends(jwt_tools.get_current_user)):
    await tools.remove_friend(current_user["id"], data.login)
    return JSONResponse(status_code=200, content={"status": "ok"})


@router.get("")
async def get_friends(
    limit: int = Query(default=1_000_000, ge=1, le=1_000_000,
                       description="Количество записей на странице"),
    offset: int = Query(
        default=0, ge=0, description="Смещение от начала списка"),
    current_user=Depends(jwt_tools.get_current_user)
):
    friends = await tools.get_friends(current_user["id"], limit=limit, offset=offset)
    return JSONResponse(status_code=200, content=friends)
