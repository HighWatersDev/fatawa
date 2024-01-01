import requests
import os
from os.path import join
import logging
from backend.config.logging_config import logging_config
from backend.utils import project_root
from dotenv import load_dotenv


logging.basicConfig(**logging_config())
logger = logging.getLogger(__name__)


ROOT_DIR = project_root.get_project_root()
config_path = f'/{ROOT_DIR}/backend/config'

dotenv_path = join(config_path, '.env')
load_dotenv(dotenv_path)

FATAWA_DB_URL = os.getenv("FATAWA_DB_URL")
FATAWA_DB_TOKEN = os.getenv("FATAWA_DB_TOKEN")

headers = {
    'Authorization': f'Bearer {FATAWA_DB_TOKEN}',
    'Content-Type': 'application/json'
}


def get_document_by_id(doc_id):
    url = f"{FATAWA_DB_URL}/documents/{doc_id}"
    try:
        response = requests.get(url, headers=headers)

        # Check for successful request
        if response.status_code == 200:
            logging.info("Document retrieved successfully")
            return response

        # Handle client errors (4xx)
        if 400 <= response.status_code < 500:
            logging.error(f"Client error: {response.status_code} - {response.json()}")
            return response.json()

        # Handle server errors (5xx)
        if 500 <= response.status_code < 600:
            logging.error(f"Server error: {response.status_code} - {response.json()}")
            return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during requests to {url} : {str(e)}")
        return None


def create_document(doc_id, document_data):
    url = f"{FATAWA_DB_URL}/documents/{doc_id}"
    try:
        response = requests.post(url, json=document_data, headers=headers)

        # Check for successful request
        if response.status_code == 200:
            logging.info("Document created successfully")
            return response

        # Handle client errors (4xx)
        if 400 <= response.status_code < 500:
            logging.error(f"Client error: {response.status_code} - {response.json()}")
            return response.json()

        # Handle server errors (5xx)
        if 500 <= response.status_code < 600:
            logging.error(f"Server error: {response.status_code} - {response.json()}")
            return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during requests to {url} : {str(e)}")
        return None


def update_document(doc_id, update_data):
    url = f"{FATAWA_DB_URL}/documents/{doc_id}"
    try:
        response = requests.put(url, json=update_data, headers=headers)

        # Check for successful request
        if response.status_code == 200:
            logging.info("Document updated successfully")
            return response

        # Handle client errors (4xx)
        if 400 <= response.status_code < 500:
            logging.error(f"Client error: {response.status_code} - {response.json()}")
            return response.json()

        # Handle server errors (5xx)
        if 500 <= response.status_code < 600:
            logging.error(f"Server error: {response.status_code} - {response.json()}")
            return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during requests to {url} : {str(e)}")
        return None


def search_documents(search_params):
    url = f"{FATAWA_DB_URL}/documents/search"
    try:
        response = requests.get(url, params=search_params, headers=headers)

        # Check for successful request
        if response.status_code == 200:
            logging.info("Documents searched successfully")
            return response

        # Handle client errors (4xx)
        if 400 <= response.status_code < 500:
            logging.error(f"Client error: {response.status_code} - {response.json()}")
            return response.json()

        # Handle server errors (5xx)
        if 500 <= response.status_code < 600:
            logging.error(f"Server error: {response.status_code} - {response.json()}")
            return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during requests to {url} : {str(e)}")
        return None


def get_all_documents():
    url = f"{FATAWA_DB_URL}/documents/all"
    try:
        response = requests.get(url, headers=headers)

        # Check for successful request
        if response.status_code == 200:
            logging.info("Documents returned successfully")
            return response

        # Handle client errors (4xx)
        if 400 <= response.status_code < 500:
            logging.error(f"Client error: {response.status_code} - {response.json()}")
            return response.json()

        # Handle server errors (5xx)
        if 500 <= response.status_code < 600:
            logging.error(f"Server error: {response.status_code} - {response.json()}")
            return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during requests to {url} : {str(e)}")
        return None


def delete_document(doc_id):
    url = f"{FATAWA_DB_URL}/documents/{doc_id}"
    try:
        response = requests.delete(url, headers=headers)

        # Check for successful request
        if response.status_code == 200:
            logging.info("Documents searched successfully")
            return response

        # Handle client errors (4xx)
        if 400 <= response.status_code < 500:
            logging.error(f"Client error: {response.status_code} - {response.json()}")
            return response.json()

        # Handle server errors (5xx)
        if 500 <= response.status_code < 600:
            logging.error(f"Server error: {response.status_code} - {response.json()}")
            return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during requests to {url} : {str(e)}")
        return None
