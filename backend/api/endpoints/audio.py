from fastapi import APIRouter, Depends, HTTPException

from backend.auth.validate_token import validate_user
from backend.utils import audio_editor
from backend.api.endpoints.storage import upload_files

router = APIRouter()


@router.get("/to_acc", dependencies=[Depends(validate_user)])
async def convert_acc(blob):
    '''
    Convert audio file to ACC format
    :param blob: path to the local wav file
    :return:
    '''
    response = await audio_editor.convert_to_acc(blob)
    if response:
        await upload_files(blob)


@router.get("/to_wav", dependencies=[Depends(validate_user)])
async def convert_wav(blob):
    response = await audio_editor.convert_to_wav(blob)
    if response:
        await upload_files(blob)