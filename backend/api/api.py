from fastapi import APIRouter

from backend.api.endpoints import audio, storage,\
    translator, transcriber


api_router = APIRouter()
api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
api_router.include_router(storage.router, prefix="/storage", tags=["storage"])
api_router.include_router(translator.router, prefix="/translator", tags=["translator"])
api_router.include_router(transcriber.router, prefix="/transcriber", tags=["transcriber"])
