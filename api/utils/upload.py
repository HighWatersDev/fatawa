from pathlib import Path
import os
from os.path import join
from azure.storage.blob import BlobServiceClient

from dotenv import load_dotenv


def get_project_root():
    root_dir = Path(__file__).absolute().parent.parent.parent
    return root_dir


ROOT_DIR = get_project_root()
dotenv_path = join(ROOT_DIR, '.env')
load_dotenv(dotenv_path)

account_url = "https://fatawaaudio.blob.core.windows.net"
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')


class DirectoryClient:
    def __init__(self, container_name):
        service_client = BlobServiceClient.from_connection_string(connection_string)
        self.client = service_client.get_container_client(container_name)

    def upload(self, source, dest):
        """
        Upload a file or directory to a path inside the container
        """
        source = f'{ROOT_DIR}/{source}'
        if os.path.isdir(source):
            self.upload_dir(source, dest)
        else:
            self.upload_file(source, dest)

    def upload_file(self, source, dest):
        """
        Upload a single file to a path inside the container
        """
        print(f'Uploading {source} to {dest}')
        with open(source, 'rb') as data:
            self.client.upload_blob(name=dest, data=data)

    def upload_dir(self, source, dest):
        """
        Upload a directory to a path inside the container
        """
        prefix = '' if dest == '' else dest + '/'
        prefix += os.path.basename(source) + '/'
        for root, dirs, files in os.walk(source):
            for name in files:
                dir_part = os.path.relpath(root, source)
                dir_part = '' if dir_part == '.' else dir_part + '/'
                file_path = os.path.join(root, name)
                blob_path = prefix + dir_part + name
                self.upload_file(file_path, blob_path)
