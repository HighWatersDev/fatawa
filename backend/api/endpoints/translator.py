from fastapi import APIRouter, Depends, HTTPException

from backend.auth.validate_token import validate_user
from backend.utils import translator

router = APIRouter()


@router.get("/translate", dependencies=[Depends(validate_user)])
async def translate_fatawa(blob: str):
    response = await translator.translate_fatawa(blob)
    if response:
        return True
    else:
        return False
