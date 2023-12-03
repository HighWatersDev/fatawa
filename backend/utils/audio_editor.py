from pydub import AudioSegment
import os
from backend.utils import project_root

root_path = project_root.get_project_root()
artifacts = f'{root_path}/artifacts'


def check_folder(folder):
    print(f'Checking if {folder} exists')
    if not os.path.isdir(f'{folder}'):
        try:
            print(f'{folder} doesn\'t exist. Creating it.')
            os.makedirs(f'{folder}')
        except Exception as err:
            print(err)
    else:
        print(f'{folder} exists. Carrying on...')


async def convert_to_wav(file_path):
    audio_file = AudioSegment.from_mp3(file_path)
    file = audio_file.replace(".mp3", "")
    try:
        audio_file.export(f'{file}.wav', format="wav", parameters=["-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000"])
        print(f'Successfully converted audio file: {file_path}')
        return True
    except Exception as err:
        print("Error: Failed to edit audio file: ", err)
        return False


async def convert_to_acc(file_path):
    try:
        file = file_path.replace(".wav", "")
        audio_file = AudioSegment.from_wav(f'{file_path}')
        acc_file = audio_file.export(f'{file}.acc', format="adts", bitrate="32k")
        print(f'Successfully converted audio file: {acc_file}')
        return True
    except Exception as err:
        print(err)
        return False
