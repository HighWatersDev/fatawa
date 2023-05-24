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


def edit_audio(file_name, folder, start_min, start_sec, end_min, end_sec, trim):
    audio_file = AudioSegment.from_mp3(f'fatwa-audio-full/{folder}/{file_name}.mp3')

    duration = ((end_min * 60 + end_sec) - (start_min * 60 + start_sec)) * 1000

    try:
        if trim:
            qna = audio_file[-duration:]
        else:
            qna = audio_file
        qna.export(f'fatwa-audio-wav/{folder}/{file_name}.wav', format="wav", parameters=["-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000"])
        print(f'Successfully converted audio file: {file_name}')
        return True
    except Exception as err:
        print("Error: Failed to edit audio file: ", err)
        return False


async def convert_to_acc(blob):
    src_folder = os.getenv("CONVERT_ACC_SRC_FOLDER", "fatwa-audio-wav")
    dst_folder = os.getenv("CONVERT_ACC_DST_FOLDER", "fatwa-audio-acc")
    check_folder(f'{artifacts}/{src_folder}/{blob}')
    check_folder(f'{artifacts}/{dst_folder}/{blob}')
    files = os.listdir(f'{artifacts}/{src_folder}/{blob}')
    try:
        for audio_file in files:
            audio_file = AudioSegment.from_wav(f'{artifacts}/{src_folder}/{blob}/{audio_file}')
            acc_file = audio_file.export(f'{artifacts}/{dst_folder}/{blob}/{audio_file}.acc', format="adts", bitrate="32k")
            print(f'Successfully converted audio file: {acc_file}')
        return True
    except Exception as err:
        print(err)
        return False
