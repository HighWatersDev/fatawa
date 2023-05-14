from fastapi import APIRouter, Depends, HTTPException

from backend.auth.validate_token import validate_user
from backend.utils.azure_storage import DirectoryClient
from backend.utils import project_root

router = APIRouter()

ROOT = project_root.get_project_root()


@router.get("/api/storage/upload", dependencies=[Depends(validate_user)])
async def upload_files(path: str):
    container = path.rsplit("/")[0]
    blob = path.rsplit("/")[1]
    client = DirectoryClient(container)
    return client.upload(path, blob)


@router.get("/api/storage/list", dependencies=[Depends(validate_user)])
async def list_files(path: str):
    container = path.rsplit("/")[0]
    blob = '/'.join(path.rsplit("/")[1:])
    client = DirectoryClient(container)
    return client.ls_files(blob)


@router.get("/api/storage/download", dependencies=[Depends(validate_user)])
async def list_files(path: str):
    container = path.rsplit("/")[0]
    blob = '/'.join(path.rsplit("/")[1:])
    client = DirectoryClient(container)
    dst = f'{ROOT}/artifacts'
    response = client.download(blob, dst)
    if response:
        return True