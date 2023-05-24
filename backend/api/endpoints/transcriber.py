from fastapi import APIRouter, Depends, HTTPException

from backend.auth.validate_token import validate_user
from backend.utils import transcriber

router = APIRouter()


@router.get("/transcribe", dependencies=[Depends(validate_user)])
async def transcribe_fatawa(blob: str):
    response = await transcriber.transcribe(blob)
    if response:
        return True
    else:
        return False
