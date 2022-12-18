# Imports the Google Cloud Translation library
from google.cloud import translate
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "focus-loader-185112-7c5ddd15d741.json"


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


file = "upload1526642374358.txt"
with open(f'transcriptions/{file}', "r") as in_file,open(f'translations/{file}', "w") as out_file:
    text = in_file.read()
    translated_text = translate_text(text=text, project_id="focus-loader-185112")
    out_file.write(translated_text)
