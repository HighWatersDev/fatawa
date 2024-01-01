import requests
import os
from os.path import join
from backend.utils import project_root
from dotenv import load_dotenv

ROOT_DIR = project_root.get_project_root()
config_path = f'/{ROOT_DIR}/backend/config'

dotenv_path = join(config_path, '.env')
load_dotenv(dotenv_path)

FATAWA_DB_URL = os.getenv("FATAWA_DB_URL")
FATAWA_DB_TOKEN = os.getenv("FATAWA_DB_TOKEN")


def get_document_by_id(doc_id):
    url = f"{FATAWA_DB_URL}/documents/{doc_id}"
    headers = {
        'Authorization': f'Bearer {FATAWA_DB_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response


def create_document(doc_id, document_data):
    url = f"{FATAWA_DB_URL}/documents/{doc_id}"
    headers = {'Authorization': f'Bearer {FATAWA_DB_TOKEN}'}
    response = requests.post(url, json=document_data, headers=headers)
    return response


def update_document(doc_id, update_data):
    url = f"{FATAWA_DB_URL}/documents/{doc_id}"
    headers = {'Authorization': f'Bearer {FATAWA_DB_TOKEN}'}
    response = requests.put(url, json=update_data, headers=headers)
    return response


def search_documents(search_params):
    url = f"{FATAWA_DB_URL}/documents/search"
    headers = {'Authorization': f'Bearer {FATAWA_DB_TOKEN}'}
    response = requests.get(url, params=search_params, headers=headers)
    return response


def get_all_documents():
    url = f"{FATAWA_DB_URL}/documents/all"
    headers = {'Authorization': f'Bearer {FATAWA_DB_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response


def verify():
    url = f"{FATAWA_DB_URL}/verify"
    headers = {'Authorization': f'Bearer {FATAWA_DB_TOKEN}'}
    response = requests.post(url, headers=headers)
    return response


def delete_document(doc_id):
    url = f"{FATAWA_DB_URL}/documents/{doc_id}"
    headers = {'Authorization': f'Bearer {FATAWA_DB_TOKEN}'}
    response = requests.delete(url, headers=headers)
    return response
