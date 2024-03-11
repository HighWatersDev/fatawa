import uvicorn
from fastapi.openapi.utils import get_openapi

from backend.api.api import api_router
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(openapi_url="/v1/processor/openapi.json")


# Set all CORS enabled origins
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/v1/processor")

if __name__ == "__main__":
    uvicorn.run("backend.main:app")