import os
import ssl
import yt_dlp

ssl._create_default_https_context = ssl._create_unverified_context


def download_video(video_url, output_path="./downloads"):
    """Download the video-only version."""
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'nocheckcertificate': True,
    }

    os.makedirs(output_path, exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_audio(video_url, output_path="./downloads"):
    """Download the audio-only version."""
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


if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ").strip()
    choice = input("Do you want to download video or audio? (v/a): ").strip().lower()

    if choice == 'v':
        download_video(video_url)
    elif choice == 'a':
        download_audio(video_url)
    else:
        print("Invalid choice. Please enter 'v' for video or 'a' for audio.")
