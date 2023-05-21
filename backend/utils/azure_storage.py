from pathlib import Path
import os
from os.path import join
from azure.storage.blob import BlobServiceClient
from backend.utils import project_root
from dotenv import load_dotenv
from azure.core.exceptions import (
    ResourceExistsError,
    ResourceNotFoundError,
    ClientAuthenticationError,
    HttpResponseError,
    ServiceResponseError,
)


ROOT_DIR = project_root.get_project_root()
artifacts = f'{ROOT_DIR}/artifacts'
config_path = f'/{ROOT_DIR}/backend/config'
dotenv_path = join(config_path, '.env')
load_dotenv(dotenv_path)

account_url = "https://fatawaaudio.blob.core.windows.net"
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Create a BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)


# Function to upload a file or folder to Azure Storage
def upload_to_azure_storage(path, destination):
    container_name = path.rsplit("/")[1]
    container_client = blob_service_client.get_container_client(container_name)
    if os.path.isfile(path):
        upload_file(path, destination, container_client)
    elif os.path.isdir(path):
        upload_folder(path, destination, container_client)


# Function to upload a file to Azure Storage
def upload_file(file_path, destination_folder_name, container_client):
    blob_name = os.path.join(destination_folder_name, os.path.basename(file_path))
    blob_client = container_client.get_blob_client(blob_name)
    try:
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)
        print(f"Uploaded file: {file_path} to blob: {blob_name}")
    except ResourceExistsError:
        print(f"Blob {blob_name} already exists. Skipping upload for file: {file_path}")
    except (ResourceNotFoundError, ClientAuthenticationError, HttpResponseError, ServiceResponseError) as ex:
        print(f"An error occurred while uploading file: {file_path}")
        print(f"Error details: {str(ex)}")


# Function to upload a folder to Azure Storage
def upload_folder(folder_path, destination_folder_name, container_client):
    for root, _, files in os.walk(folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            destination_blob_name = os.path.join(destination_folder_name, local_file_path[len(folder_path) + 1:])
            upload_file(local_file_path, destination_blob_name, container_client)
    print(f"Uploaded folder: {folder_path} to blob: {destination_folder_name}")


# Function to download a file from Azure Storage
def download_file(blob_path, destination):
    container_name = blob_path.rsplit("/")[1]
    container_client = blob_service_client.get_container_client(container_name)
    local_file_path = os.path.join(destination, os.path.basename(blob_path))
    blob_client = container_client.get_blob_client(blob_path)
    try:
        with open(local_file_path, "wb") as file:
            data = blob_client.download_blob()
            data.readinto(file)
        print(f"Downloaded blob: {blob_path} to file: {local_file_path}")
    except (ResourceNotFoundError, ClientAuthenticationError, HttpResponseError, ServiceResponseError) as ex:
        print(f"An error occurred while downloading blob: {blob_path}")
        print(f"Error details: {str(ex)}")


# Function to list files inside a blob
def list_files(blob):
    container_name = blob.rsplit("/")[0]
    container_client = blob_service_client.get_container_client(container_name)
    blob_name = blob.rsplit("/")[1]
    blob_client = container_client.get_blob_client(blob_name)
    try:
        blob_client.get_blob_properties()
        print(f"Files inside blob: {blob_name}:")
        for blob in container_client.list_blobs(name_starts_with=blob_name):
            print(blob.name)
    except (ResourceNotFoundError, ClientAuthenticationError, HttpResponseError, ServiceResponseError) as ex:
        print(f"An error occurred while listing files in blob: {blob_name}")
        print(f"Error details: {str(ex)}")
