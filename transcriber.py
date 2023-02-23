import json
import string
import time
import threading
import wave
import uuid
import os
from os.path import join, dirname
from api.utils.utils import az_main, az_upload

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SERVICE_REGION")

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)


def check_folder(folder):
    print(f'Checking if {folder} exists')
    if not os.path.isdir(f'transcriptions/{folder}'):
        print(f'{folder} doesn\'t exist. Creating it.')
        os.makedirs(f'transcriptions/{folder}')
    else:
        print(f'{folder} exists. Carrying on...')


def download_files(scholar, folder):
    container = "cut-audio-files"
    path = f'{scholar}/{folder}'
    return az_main(container, path)


def speech_recognize_cont(speech_key, service_region, container, audio_file, scholar, folder):

    transcript_file = f'{audio_file}.txt'
    audio_file_path = f'{container}/{scholar}/{folder}/{audio_file}'
    transcription_path = f'transcriptions/{scholar}/{folder}/{transcript_file}'
    try:
        os.makedirs(os.path.dirname(transcription_path), exist_ok=True)
    except Exception:
        exit(1)
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.output_format = speechsdk.OutputFormat.Detailed
    speech_config.set_property_by_name("DifferentiateGuestSpeakers", "true")
    speech_config.request_word_level_timestamps()
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config,
                                                   language="ar-SA")

    done = False
    text = []
    print("Recognizing...")

    def recognized(evt: speechsdk.SessionEventArgs):
        #             result.append(evt.result.text)
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(evt))
            print("Offset: {}".format(evt.result.offset))
            text.append(evt.result.text)
            with open(transcription_path, "a") as f:
                f.write(evt.result.text)
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(evt.result.no_match_details))
        elif evt.result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = evt.result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

        return text

    #         def start(evt):
    #             print('SESSION STARTED: {}'.format(evt))

    def stop(evt: speechsdk.SessionEventArgs):
        print('CLOSING on {}'.format(evt))
        if evt.result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = evt.result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    #         speech_recognizer.recognizing.connect(lambda evt)
    speech_recognizer.recognized.connect(recognized)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    #         speech_recognizer.session_started.connect(start)
    speech_recognizer.session_stopped.connect(stop)
    speech_recognizer.canceled.connect(stop)

    # Start continuous speech recognition
    try:
        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)

        speech_recognizer.stop_continuous_recognition()

    except KeyboardInterrupt:
        print("bye.")
        speech_recognizer.recognized.disconnect_all()
        speech_recognizer.session_started.disconnect_all()
        speech_recognizer.session_stopped.disconnect_all()


async def az_transcribe(container, scholar, folder):
    if download_files(scholar, folder):
        for audio_file in os.listdir(f'{container}/{scholar}/{folder}'):
            try:
                speech_recognize_cont(speech_key, service_region, audio_file, scholar, folder)
                az_upload("transcriptions", f'{scholar}/{folder}/{audio_file}.txt')
            except Exception as err:
                return err
