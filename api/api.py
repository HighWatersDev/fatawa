import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Optional, List
#from utils import az_list_containers, az_list_blobs
from utils.azstorage import DirectoryClient
import tempfile
from utils.project_root import get_project_root
from utils import transcriber
#from transcriber import az_transcribe

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

allow_all = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all
)


# @app.get("/api/transcribe/")
# async def get_files(scholar: str, folder: str):
#     return await az_transcribe("acc-audio-files", scholar, folder)


@app.get("/api/storage/upload")
async def upload_files(path: str):
    container = path.rsplit("/")[0]
    blob = path.rsplit("/")[1]
    client = DirectoryClient(container)
    return client.upload(path, blob)


@app.get("/api/storage/list")
async def list_files(path: str):
    container = path.rsplit("/")[0]
    blob = '/'.join(path.rsplit("/")[1:])
    client = DirectoryClient(container)
    return client.ls_files(blob)


@app.get("/api/storage/download")
async def list_files(path: str):
    container = path.rsplit("/")[0]
    blob = '/'.join(path.rsplit("/")[1:])
    client = DirectoryClient(container)
    with tempfile.TemporaryDirectory(dir=get_project_root()) as tmpdir:
        response = client.download(blob, tmpdir)
    if response:
        return tmpdir


@app.get("/api/transcribe")
async def transcribe_fatawa(blob: str):
    response = await transcriber.transcribe(blob)
    if response:
        return True
    else:
        return False


if __name__ == "__main__":
    uvicorn.run("utils_api:app")
