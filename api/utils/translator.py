# Imports the Google Cloud Translation library
from google.cloud import translate
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_translate_api.json"


def check_folder(folder):
    print(f'Checking if {folder} exists')
    if not os.path.isdir(f'translations/{folder}'):
        print(f'{folder} doesn\'t exist. Creating it.')
        os.makedirs(f'translations/{folder}')
    else:
        print(f'{folder} exists. Carrying on...')


# Initialize Translation client
def translate_text(text="YOUR_TEXT_TO_TRANSLATE", project_id="YOUR_PROJECT_ID"):
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


def save_translation(file, folder):
    check_folder(folder)
    try:
        with open(f'transcriptions/{folder}/{file}', "r") as in_file,\
                open(f'translations/{folder}/{file}', "w") as out_file:
            text = in_file.read()
            translated_text = translate_text(text=text, project_id="salafifatawa")
            out_file.write(translated_text)
        return True
    except Exception as err:
        print(err)
        return False
