from fastapi import APIRouter, Depends

from backend.auth.validate_token import validate_user
from backend.utils.azure_storage import upload_to_azure_storage, download_file, list_files
from backend.utils import project_root

router = APIRouter()

ROOT = project_root.get_project_root()


@router.post("/upload", dependencies=[Depends(validate_user)])
async def upload_files(path: str):
    blob = path.rsplit("/")[2]
    return upload_to_azure_storage(path, blob)


@router.get("/list", dependencies=[Depends(validate_user)])
async def list_files(path: str):
    return list_files(path)


@router.get("/download", dependencies=[Depends(validate_user)])
async def download(file_path: str, destination_path: str):
    response = download_file(file_path, destination_path)
    if response:
        return True
