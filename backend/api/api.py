from fastapi import FastAPI, HTTPException
from typing import Optional, List
from backend.utils.azstorage import DirectoryClient
from backend.utils import transcriber, translator, project_root, audio_editor
import secure
import uvicorn
from backend.auth.config import settings
from backend.auth.dependencies import PermissionsValidator, validate_token
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


from fastapi.middleware.cors import CORSMiddleware

ROOT = project_root.get_project_root()

app = FastAPI(openapi_url=None)

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


csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
referrer = secure.ReferrerPolicy().no_referrer()
cache_value = secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate()
x_frame_options = secure.XFrameOptions().deny()

secure_headers = secure.Secure(
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    cache=cache_value,
    xfo=x_frame_options,
)


@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_origin_url],
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=86400,
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    message = str(exc.detail)

    return JSONResponse({"message": message}, status_code=exc.status_code)


@app.get("/api/messages/public")
def public():
    return {"text": "This is a public message."}


@app.get("/api/messages/protected", dependencies=[Depends(validate_token)])
def protected():
    return {"text": "This is a protected message."}


@app.get(
    "/api/messages/admin",
    dependencies=[Depends(PermissionsValidator(["read:admin-messages"]))],
)
def admin():
    return {"text": "This is an admin message."}