from fastapi import FastAPI, HTTPException
from typing import Optional, List
from backend.utils.azstorage import DirectoryClient
from backend.utils import transcriber, translator, project_root, audio_editor
import tempfile

from fastapi.middleware.cors import CORSMiddleware

ROOT = project_root.get_project_root()

app = FastAPI()

allow_all = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all
)


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
    dst = f'{ROOT}/artifacts'
    response = client.download(blob, dst)
    if response:
        return True


@app.get("/api/transcribe")
async def transcribe_fatawa(blob: str):
    response = await transcriber.transcribe(blob)
    if response:
        return True
    else:
        return False


@app.get("/api/translate")
async def translate_fatawa(blob: str):
    response = await translator.translate_fatawa(blob)
    if response:
        return True
    else:
        return False


@app.get("/api/audio/convert")
async def convert_acc(blob):
    response = await audio_editor.convert_to_acc(blob)
    if response:
        await upload_files(blob)
