from pydub import AudioSegment

audio_file_name = "upload1526642374358"
audio_file = AudioSegment.from_mp3(f'full_audio_files/{audio_file_name}.mp3')

start_min = 41
start_sec = 13
end_min = 54
end_sec = 45

duration = ((end_min * 60 + end_sec) - (start_min * 60 + start_sec)) * 1000

qna = audio_file[-duration:]

qna.export(f'cut_audio_files/{audio_file_name}.wav', format="wav", parameters=["-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000"])
