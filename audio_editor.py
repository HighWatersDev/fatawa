from pydub import AudioSegment
import os


def check_folder(folder):
    print(f'Checking if {folder} exists')
    if not os.path.isdir(f'acc_audio_files/{folder}'):
        try:
            print(f'{folder} doesn\'t exist. Creating it.')
            os.makedirs(f'acc_audio_files/{folder}')
        except Exception as err:
            print(err)
    else:
        print(f'{folder} exists. Carrying on...')


def edit_audio(file_name, folder, start_min, start_sec, end_min, end_sec, trim):
    audio_file = AudioSegment.from_mp3(f'full_audio_files/{folder}/{file_name}.mp3')

    duration = ((end_min * 60 + end_sec) - (start_min * 60 + start_sec)) * 1000

    try:
        if trim:
            qna = audio_file[-duration:]
        else:
            qna = audio_file
        qna.export(f'cut_audio_files/{folder}/{file_name}.wav', format="wav", parameters=["-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000"])
        print(f'Successfully converted audio file: {file_name}')
        return True
    except Exception as err:
        print("Error: Failed to edit audio file: ", err)
        return False


def convert_to_acc(file_name, folder):
    check_folder(folder)
    try:
        audio_file = AudioSegment.from_wav(f'cut_audio_files/{folder}/{file_name}')
        acc_file = audio_file.export(f'acc_audio_files/{folder}/{file_name}.acc', format="adts", bitrate="32k")
        print(f'Successfully converted audio file: {acc_file}')
        return True
    except Exception as err:
        print(err)
        return False
