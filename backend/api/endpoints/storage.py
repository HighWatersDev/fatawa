from fastapi import APIRouter, Depends

from backend.auth.validate_token import validate_user
from backend.utils.azure_storage import upload_to_azure_storage, download_file, list_files
from backend.utils import project_root

router = APIRouter()

ROOT = project_root.get_project_root()


@router.post("/upload", dependencies=[Depends(validate_user)])
async def upload_files(path: str, author: str):
    return upload_to_azure_storage(path, author)


@router.get("/list", dependencies=[Depends(validate_user)])
async def list_blob(path: str):
    file_list = list_files(path)
    if file_list is None:
        # Handle the error condition
        return {"message": "An error occurred while listing files in blob"}
    return {"files": file_list}


@router.get("/download", dependencies=[Depends(validate_user)])
async def download(file_path: str, author: str):
    response = download_file(file_path, author)
    if response:
        return True
