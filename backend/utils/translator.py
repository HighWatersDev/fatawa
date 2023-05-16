# Imports the Google Cloud Translation library
from google.cloud import translate
import os
from os.path import join, dirname
from backend.utils.project_root import get_project_root

from dotenv import load_dotenv

config_path = f'{get_project_root()}/backend/config'
dotenv_path = join(config_path, '.env')
load_dotenv(dotenv_path)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f'{config_path}/gcp_translate_api.json'
project_id = os.getenv("GCP_PROJECT_ID", "salafifatawa")
src_folder = os.getenv("TRANSCRIBER_SRC_FOLDER", "fatwa-transcription")
dst_folder = os.getenv("TRANSCRIBER_DST_FOLDER", "fatwa-translation")
root_path = f'{get_project_root()}/artifacts'


def check_folder():
    folders = [src_folder, dst_folder]
    for folder in folders:
        print(f'Checking if {folder} exists')
        if not os.path.isdir(f'{root_path}/{folder}'):
            print(f'{folder} doesn\'t exist. Creating it.')
            os.makedirs(f'{root_path}/{folder}')
        else:
            print(f'{folder} exists. Carrying on...')


# Initialize Translation client
def translate_text(text="YOUR_TEXT_TO_TRANSLATE"):
    """Translating Text."""

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "ar-SA",
            "target_language_code": "en-US",
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print("Translated text: {}".format(translation.translated_text))
        return translation.translated_text


async def translate_fatawa(blob):
    check_folder()
    try:
        transcription_path = f'{root_path}/{src_folder}/{blob}'
        translation_path = f'{root_path}/{dst_folder}/{blob}'
        os.makedirs(os.path.dirname(transcription_path), exist_ok=True)
        os.makedirs(os.path.dirname(translation_path), exist_ok=True)
        files = os.listdir(transcription_path)
        for file in files:
            with open(f'{root_path}/{src_folder}/{blob}/{file}', "r") as in_file,\
                    open(f'{root_path}/{dst_folder}/{blob}/{file}', "w") as out_file:
                text = in_file.read()
                translated_text = translate_text(text=text)
                out_file.write(translated_text)
        return True
    except Exception as err:
        print(err)
        return False
