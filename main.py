import os
from os.path import join, dirname
import audio_editor as ae
import transcriber as trc
import translator as trl

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

start_min = 45
start_sec = 49
end_min = 60
end_sec = 28
file_name = "33827"
speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SERVICE_REGION")
audio_file = "33827.wav"
folder = "albadr"
trim = False


if __name__ == "__main__":
    if ae.edit_audio(file_name, folder, start_min, start_sec, end_min, end_sec, trim):
        response = input("Is audio file ready for transcription?\n")
        if response == "y":
            trc.speech_recognize_cont(speech_key, service_region, audio_file, folder)
    response = input("Is transcription ready for translation?\n")
    if response == "y":
        trl.save_translation(f'{audio_file}.txt', folder)
