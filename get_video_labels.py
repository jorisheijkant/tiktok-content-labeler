import os
from functions import download_from_zeeschuimer_csv, transcribe_with_whisper, get_video_themes

csv_path = 'data/godfluencers.csv'
project_name = 'godfluencer'
whisper_model = 'turbo'
language = 'nl'
num_themes = 5
max_videos_to_download = 1000

video_folder_path = f"data/{project_name}"
os.makedirs(video_folder_path, exist_ok=True)

#download_from_zeeschuimer_csv(csv_path, video_folder_path, max_videos_to_download)
# transcribe_with_whisper(video_folder_path, whisper_model, language)
get_video_themes(video_folder_path, num_themes)
