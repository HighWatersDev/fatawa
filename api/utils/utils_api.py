import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Optional, List
from utils import az_list_containers, az_list_blobs
from upload import DirectoryClient
import transcriber as trc
from transcriber import az_transcribe

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



@app.get("/api/folders")
async def get_todo():
    response = await az_list_containers()
    return response


@app.get("/api/transcribe/")
async def get_files(scholar: str, folder: str):
    return await az_transcribe("acc-audio-files", scholar, folder)


@app.get("/api/upload")
async def upload_files(path: str):
    container = path.rsplit("/")[0]
    blob = path.rsplit("/")[1]
    client = DirectoryClient(container)
    return client.upload(path, blob)

if __name__ == "__main__":
    uvicorn.run("utils_api:app")

# @app.post("/api/todo/", response_model=Todo)
# async def post_todo(todo: Todo):
#     response = await create_todo(todo.dict())
#     if response:
#         return response
#     raise HTTPException(400, "Something went wrong")
#
#
# @app.put("/api/todo/{title}/", response_model=Todo)
# async def put_todo(title: str, desc: str):
#     response = await update_todo(title, desc)
#     if response:
#         return response
#     raise HTTPException(404, f"There is no todo with the title {title}")
