from fastapi import APIRouter, Depends, HTTPException

from backend.auth.validate_token import validate_user
from backend.utils import audio_editor
from backend.api.endpoints.storage import upload_files

router = APIRouter()


@router.get("/api/audio/convert", dependencies=[Depends(validate_user)])
async def convert_acc(blob):
    response = await audio_editor.convert_to_acc(blob)
    if response:
        await upload_files(blob)