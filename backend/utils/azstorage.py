from pathlib import Path
import os
from os.path import join
from azure.storage.blob import BlobServiceClient
from backend.utils import project_root
from dotenv import load_dotenv


ROOT_DIR = f'{project_root.get_project_root()}/artifacts'
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
        try:
            print(f'Uploading {source} to {dest}')
            with open(source, 'rb') as data:
                self.client.upload_blob(name=dest, data=data)
            return True
        except Exception:
            return False

    def upload_dir(self, source, dest):
        """
        Upload a directory to a path inside the container
        """
        try:
            prefix = '' if dest == '' else dest + '/'
            prefix += os.path.basename(source) + '/'
            for root, dirs, files in os.walk(source):
                for name in files:
                    dir_part = os.path.relpath(root, source)
                    dir_part = '' if dir_part == '.' else dir_part + '/'
                    file_path = os.path.join(root, name)
                    blob_path = prefix + dir_part + name
                    self.upload_file(file_path, blob_path)
            return True
        except Exception:
            return False

    def download(self, source, dest):
        """
        Download a file or directory to a path on the local filesystem
        """
        if not dest:
            raise Exception('A destination must be provided')
        dest = f'{ROOT_DIR}/{dest}'

        blobs = self.ls_files(source, recursive=True)
        if blobs:
            # if source is a directory, dest must also be a directory
            if not source == '' and not source.endswith('/'):
                source += '/'
            if not dest.endswith('/'):
                dest += '/'
            # append the directory name from source to the destination
            dest += os.path.basename(os.path.normpath(source)) + '/'

            blobs = [source + blob for blob in blobs]
            for blob in blobs:
                blob_dest = dest + os.path.relpath(blob, source)
                self.download_file(blob, blob_dest)
        else:
            self.download_file(source, dest)

    def download_file(self, source, dest):
        """
        Download a single file to a path on the local filesystem
        """
        # dest is a directory if ending with '/' or '.', otherwise it's a file
        if dest.endswith('.'):
            dest += '/'
        blob_dest = dest + os.path.basename(source) if dest.endswith('/') else dest

        print(f'Downloading {source} to {blob_dest}')
        os.makedirs(os.path.dirname(blob_dest), exist_ok=True)
        bc = self.client.get_blob_client(blob=source)
        if not dest.endswith('/'):
            with open(blob_dest, 'wb') as file:
                data = bc.download_blob()
                file.write(data.readall())

    def ls_files(self, path, recursive=False):
        """
        List files under a path, optionally recursively
        """
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.client.list_blobs(name_starts_with=path)
        files = []
        for blob in blob_iter:
            relative_path = os.path.relpath(blob.name, path)
            if recursive or not '/' in relative_path:
                files.append(relative_path)
        return files

    def ls_dirs(self, path, recursive=False):
        """
        List directories under a path, optionally recursively
        """
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.client.list_blobs(name_starts_with=path)
        dirs = []
        for blob in blob_iter:
            relative_dir = os.path.dirname(os.path.relpath(blob.name, path))
            if relative_dir and (recursive or not '/' in relative_dir) and not relative_dir in dirs:
                dirs.append(relative_dir)

        return dirs
