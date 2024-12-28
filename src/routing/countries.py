from fastapi import APIRouter
from fastapi.responses import JSONResponse

from db import tools


router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("/")
async def get_countries(region: str | None = None):
    # TODO: add errorResponse
    countries = await tools.get_countries(region)
    return JSONResponse(status_code=200, content=countries)

@router.get("/{alpha2}")
async def get_country(alpha2: str):
    country = await tools.get_country(alpha2)
    if not country:
        # TODO: add errorResponse
        return JSONResponse(status_code=404, content={})
    return country
