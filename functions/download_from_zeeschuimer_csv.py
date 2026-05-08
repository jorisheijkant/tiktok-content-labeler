import csv
import subprocess
from pathlib import Path


def download_from_zeeschuimer_csv(csv_path, output_folder, max_videos=None):
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    video_urls = _parse_video_urls(csv_path)
    downloaded = 0
    for video_id, url in video_urls:
        if max_videos is not None and downloaded >= max_videos:
            break
        if not _is_already_downloaded(video_id, output_folder):
            success = _download_video(url, output_folder)
            if success:
                downloaded += 1


def _parse_video_urls(csv_path):
    seen_ids = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            video_id = row.get('item_id', '').strip()
            url = row.get('source_platform_url', '').strip()
            if video_id and url and '/video/' in url:
                seen_ids[video_id] = url
    return list(seen_ids.items())


def _is_already_downloaded(video_id, output_folder):
    return any(Path(output_folder).glob(f"{video_id}.*"))


def _download_video(url, output_folder):
    try:
        subprocess.run([
            'yt-dlp',
            '--output', str(Path(output_folder) / '%(id)s.%(ext)s'),
            '--no-playlist',
            '--quiet',
            '--progress',
            url
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Download failed for {url}: {e}")
        return False
