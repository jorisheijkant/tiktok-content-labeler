import whisper
from pathlib import Path


VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mkv', '.mov', '.m4a', '.mp3', '.wav'}


def transcribe_with_whisper(videos_folder, model_name='turbo', language=None):
    model = whisper.load_model(model_name)
    video_paths = _find_untranscribed_videos(videos_folder)
    for video_path in video_paths:
        _transcribe_video(model, video_path, language)


def _find_untranscribed_videos(folder):
    return [
        p for p in Path(folder).iterdir()
        if p.suffix.lower() in VIDEO_EXTENSIONS
        and not p.with_suffix('.txt').exists()
    ]


def _transcribe_video(model, video_path, language):
    result = model.transcribe(str(video_path), language=language, verbose=False)
    transcript_path = video_path.with_suffix('.txt')
    transcript_path.write_text(result['text'], encoding='utf-8')
