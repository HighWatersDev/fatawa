import json
import string
import time
import threading
import wave
import uuid
import os


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


def speech_recognize_cont(speech_key, service_region, audio_file, folder):
    transcript_file = f'{audio_file}.txt'
    audio_file_path = f'cut_audio_files/{folder}/{audio_file}'
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
            with open(f'transcriptions/{folder}/{transcript_file}', "a") as f:
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
