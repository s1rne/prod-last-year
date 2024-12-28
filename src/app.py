from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config import host, port
from db.session import run_database
from routing import all_routers


async def on_startup(app: FastAPI):
    await run_database()

    yield

app = FastAPI(title="s1rne prod api", lifespan=on_startup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # TODO: add errorResponse
    # TODO: add 401 token error
    return JSONResponse(
        status_code=400,
        content={},
    )


for router in all_routers:
    app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
