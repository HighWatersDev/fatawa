import os
from os.path import join, dirname
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

account_url = "https://fatawaaudio.blob.core.windows.net"
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')


def upload_audio(folder, file):

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        blob_client = blob_service_client.get_blob_client(container=folder, blob=file)

        # Upload the created file
        print("\nUploading to Azure Storage as blob:\n\t" + file)
        with open(file=f'cut_audio_files/{folder}/{file}', mode="rb") as data:
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
