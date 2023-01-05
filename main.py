import os
from os.path import join, dirname
import audio_editor as ae
import transcriber as trc
import translator as trl
import audio_storage as stor
import build_mdx as mdx

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

start_min = 58
start_sec = 23
end_min = 72
end_sec = 56
file_name = "upload1527420756581"
folder = "ruhayli"
audio_file = f'{file_name}.wav'
audio_link = f'https://fatawaaudio.blob.core.windows.net/{folder}/{audio_file}'
speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SERVICE_REGION")
trim = True

# mdx.build_fatawa_ar(folder, f'{audio_file}.txt', audio_link)
# mdx.build_fatawa_en(folder, f'{audio_file}.txt')

if __name__ == "__main__":
    if ae.edit_audio(file_name, folder, start_min, start_sec, end_min, end_sec, trim):
        response = input("Is audio file ready for transcription?\n")
        if response == "y":
            trc.speech_recognize_cont(speech_key, service_region, audio_file, folder)
    response = input("Is transcription ready for translation?\n")
    if response == "y":
        trl.save_translation(f'{audio_file}.txt', folder)
    response = input("Is audio ready to be uploaded?\n")
    if response == "y":
        stor.upload_audio(folder, audio_file)
    response = input("Is it ready to build template?\n")
    if response == "y":
        mdx.build_fatawa_ar(folder, f'{audio_file}.txt', audio_link)
        mdx.build_fatawa_en(folder, f'{audio_file}.txt')
