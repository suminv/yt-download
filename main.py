import os
import re
import ssl
import yt_dlp

ssl._create_default_https_context = ssl._create_unverified_context


def download_items(input_source, output_path="./downloads"):
    """Download videos from a playlist URLs or single URL.
    :param input_source: Playlist URL or file path with video URLs.
    :param output_path: Path to save downloads."""
    if not is_valid_youtube_url(input_source):
        print('Invalid YouTube URL. Please check the link')
        return

    resolution = select_resolution()
    ydl_opts = {
        'format': resolution,
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'nocheckcertificate': True,
        'ignoreerrors': True,  # Continue downloading if one video fails,
        'no_warnings': True,  # Suppress warnings
        'retries': 3,  # Number of download retries
        'fragment_retries': 3,  # Number of fragment download retries
        'wait_for_video': (1, 8),  # Wait between 1 and 8 seconds between retries
    }

    os.makedirs(output_path, exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([input_source])
        print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_audio(video_url, output_path="./downloads"):
    """Download the audio-only version."""
    if not is_valid_youtube_url(video_url):
        print('Invalid YouTube URL. Please check the link')
        return

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'nocheckcertificate': True,
    }

    os.makedirs(output_path, exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Audio download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


def select_resolution():
    print("Available resolutions:")
    print("1. 1080p")
    print("2. 720p")
    print("3. 480p")
    print("4. Best available")
    choice = input("Select resolution (1/2/3/4): ").strip()

    if choice == '1':
        return 'bestvideo[height<=1080]+bestaudio/best'
    elif choice == '2':
        return 'bestvideo[height<=720]+bestaudio/best'
    elif choice == '3':
        return 'bestvideo[height<=480]+bestaudio/best'
    elif choice == '4':
        return 'bestvideo+bestaudio/best'
    else:
        return 'best'


def is_valid_youtube_url(url):
    """Validate Youtube URL format"""
    youtube_regex = (
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return re.match(youtube_regex, url) is not None


def list_available_formats(url):
    """Lists the available formats for a given YouTube video URL."""
    ydl_opts = {'listformats': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        for f in formats:
            print(f"Format Code: {f.get('format_id', 'N/A')}, "
                  f"Resolution: {f.get('resolution', 'N/A')}, "
                  f"Ext: {f.get('ext', 'N/A')}")


if __name__ == "__main__":
    choice = input("Download playlist / single video or audio? (ps/a): ").strip().lower()
    if choice == 'ps':
        playlist_url = input("Enter the YouTube playlist URL or single URL: ").strip()
        download_items(playlist_url)

    elif choice == 'a':
        video_url = input("Enter the YouTube video URL for download audio: ").strip()
        download_audio(video_url)
    else:
        print("Invalid choice. Please enter 'p' for playlist or 'f' for single video or 'a' for audio.")
