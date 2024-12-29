from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from db import tools
from schemas.posts import NewPostRequest
from utils.jwt import jwt_tools
from utils.utils import collect_post_data

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/new")
async def new_post(data: NewPostRequest, current_user=Depends(jwt_tools.get_current_user)):
    post_data = await tools.new_post(current_user["id"], data)
    user = await tools.get_user_by_id(post_data["user_id"])

    post = collect_post_data(post_data)
    return JSONResponse(status_code=200, content=post)


@router.get("/{post_id}")
async def get_post(post_id: str, current_user=Depends(jwt_tools.get_current_user)):
    status, post_data = await tools.get_post_by_id(post_id, current_user["id"])
    # TODO: add normal errorResponse
    if status == 1:
        return JSONResponse(status_code=404, content={"reason": "Post not found"})
    if status == 2:
        return JSONResponse(status_code=404, content={"reason": "User not found"})
    if status == 3:
        return JSONResponse(status_code=403, content={"reason": "You are not allowed to see this post"})
    post = collect_post_data(post_data)
    return JSONResponse(status_code=200, content=post)


@router.get("/feed/my")
async def get_my_feed(
    limit: int = Query(default=1_000_000, ge=1, le=1_000_000,
                       description="Количество записей на странице"),
    offset: int = Query(
        default=0, ge=0, description="Смещение от начала списка"),
    current_user=Depends(jwt_tools.get_current_user)
):
    posts_data = await tools.get_posts_my(current_user["id"], limit=limit, offset=offset)
    posts = [collect_post_data(post) for post in posts_data]
    return JSONResponse(status_code=200, content=posts)


@router.get("/feed/{login}")
async def get_feed(
    login: str,
    limit: int = Query(default=1_000_000, ge=1, le=1_000_000,
                       description="Количество записей на странице"),
    offset: int = Query(
        default=0, ge=0, description="Смещение от начала списка"),
    current_user=Depends(jwt_tools.get_current_user)
):
    status, posts_data = await tools.get_feed_by_login(login, current_user["id"], limit=limit, offset=offset)
    if status == 2:
        return JSONResponse(status_code=404, content={"reason": "User not found"})
    if status == 3:
        return JSONResponse(status_code=404, content={"reason": "You are not allowed to see this feed"})
    
    posts = [collect_post_data(post) for post in posts_data]
    return JSONResponse(status_code=200, content=posts)


@router.get("/{post_id}/like")
async def like_post(
    post_id: str,
    current_user=Depends(jwt_tools.get_current_user)
):
    # TODO: add logic
    return JSONResponse(status_code=200, content={})


@router.get("/{post_id}/dislike")
async def dislike_post(
    post_id: str,
    current_user=Depends(jwt_tools.get_current_user)
):
    # TODO: add logic
    return JSONResponse(status_code=200, content={})
