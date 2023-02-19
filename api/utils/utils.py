import os
from pathlib import Path
import os
from os.path import join, dirname
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from dotenv import load_dotenv


def get_project_root():
    root_dir = Path(__file__).absolute().parent.parent.parent
    return root_dir


ROOT_DIR = get_project_root()
dotenv_path = join(ROOT_DIR, '.env')
load_dotenv(dotenv_path)

account_url = "https://fatawaaudio.blob.core.windows.net"
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


def az_list_containers(folder="acc-audio-files", path="ruhayli/upload1111111/1.wav.acc"):
    containers = []
    list_container = blob_service_client.list_containers()
    for container in list_container:
        container_client = blob_service_client.get_container_client(container['name'])
        for blob in container_client.list_blobs():
            folder_path = join(container['name'], blob['name']).rsplit('/')[:-1]
            if folder_path not in containers:
                containers.append(folder_path)

    return containers


def az_list_blobs(container="CONTAINER", path="SCHOLAR/FOLDER"):
    container_client = blob_service_client.get_container_client(container)
    blob_list = container_client.list_blobs()
    blobs = []
    for blob in blob_list:
        name = blob.name
        scholar, folder = name.split("/")[:2]
        blob_path = f'{scholar}/{folder}'
        if path == blob_path:
            blobs.append(blob.name)
    return blobs


def az_download_blobs(container, blobs, path):
    container_client = blob_service_client.get_container_client(container)
    for blob in blobs:
        blob_client = container_client.get_blob_client(blob)
        with open(path, "wb") as my_blob:
            download_stream = blob_client.download_blob()
            my_blob.write(download_stream.readall())


def az_store_upload(folder, file):
    try:
        blob_client = blob_service_client.get_blob_client(container=folder, blob=file)

        # Upload the created file
        print("\nUploading to Azure Storage as blob:\n\t" + file)
        with open(file=f'{ROOT_DIR}/{folder}/{file}', mode="rb") as data:
            blob_client.upload_blob(data)
            print("File has been uploaded")

    except Exception as err:
        print(err)

    try:
        container_client = blob_service_client.get_container_client(folder)

        blob_list = container_client.list_blobs()
        for blob in blob_list:
            if blob:
                print(f'Blob {blob.name} is found')
            else:
                print(f'Blob {blob.name} was not found')
                exit(1)
    except Exception as err:
        print(err)


def upload_audio(folder, file):

    try:
        blob_client = blob_service_client.get_blob_client(container=folder, blob=file)

        # Upload the created file
        print("\nUploading to Azure Storage as blob:\n\t" + file)
        with open(file=f'acc_audio_files/{folder}/{file}', mode="rb") as data:
            blob_client.upload_blob(data)
            print("File has been uploaded")

    except Exception as err:
        print(err)

    try:
        container_client = blob_service_client.get_container_client(folder)

        blob_list = container_client.list_blobs()
        for blob in blob_list:
            if blob:
                print(f'Blob {blob.name} is found')
            else:
                print(f'Blob {blob.name} was not found')
                exit(1)
    except Exception as err:
        print(err)


def make_dirs(scholar: str, folder: str):
    dirs = ['acc_audio_files', 'cut_audio_files', 'transcriptions', 'translations', 'wrong']
    for dir in dirs:
        dir_path = Path(get_project_root(), dir).joinpath()
        if dir_path.is_dir():
            print(dir_path)


def az_main(container="CONTAINER", path="SCHOLAR/FOLDER"):
    blobs = az_list_blobs(container, path)
    local_blob_path = f'{ROOT_DIR}/{container}/{path}'
    az_download_blobs(container, blobs, local_blob_path)