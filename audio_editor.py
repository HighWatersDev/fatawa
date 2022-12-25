from pydub import AudioSegment


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
