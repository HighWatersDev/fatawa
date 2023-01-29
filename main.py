import os
from os.path import join, dirname
import audio_editor as ae
import transcriber as trc
import translator as trl
import audio_storage as stor
import build_mdx as mdx
import re

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

folder = "ruhayli/upload1527509523166"
speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SERVICE_REGION")

if __name__ == "__main__":
    response = input("Audio files ready for transcription?\n")
    if response == "y":
        files = sorted(os.listdir(f'cut_audio_files/{folder}'), key=lambda x: int(os.path.splitext(x)[0]))
        for audio_file in files:
            audio_link = f'https://fatawaaudio.blob.core.windows.net/{folder}/{audio_file}.acc'
            trc.speech_recognize_cont(speech_key, service_region, audio_file, folder)
            response = input("Is transcription ready for translation?\n")
            if response == "y":
                trl.save_translation(f'{audio_file}.txt', folder)
            response = input("Is audio ready to be converted and uploaded?\n")
            if response == "y":
                ae.convert_to_acc(audio_file, folder)
                stor.upload_audio(folder, f'{audio_file}.acc')
            response = input("Is it ready to build template?\n")
            if response == "y":
                mdx.build_fatawa(folder, f'{audio_file}.txt', audio_link)
