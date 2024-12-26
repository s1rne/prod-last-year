from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from db import tools
from utils.jwt import jwt_tools
from utils.utils import collect_user_data

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{login}")
async def profile(login: str, current_user=Depends(jwt_tools.get_current_user)):
    user = await tools.get_user(login)
    if not user or user["isPublic"] is False:
        return JSONResponse(status_code=403, content={})

    content = collect_user_data(user)
    return JSONResponse(status_code=200, content=content)
