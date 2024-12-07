import os
import ssl
import yt_dlp

# Use updated certificates from certifi
ssl._create_default_https_context = ssl._create_unverified_context


def download_video(video_url, output_path="./downloads"):
    """Download the video with the best quality."""
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Best video and audio quality
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Save file with video title
        'merge_output_format': 'mp4',  # Merge video and audio into MP4
        'nocheckcertificate': True,  # Ignore SSL certificate issues
    }

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Download video
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_audio(video_url, output_path="./downloads"):
    """Download the audio-only version."""
    ydl_opts = {
        'format': 'bestaudio',  # Best available audio format
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Save file with video title
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',  # Convert to MP3
            'preferredquality': '192',  # Set audio quality
        }],
        'nocheckcertificate': True,  # Ignore SSL certificate issues
    }

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Download audio
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Audio download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Get user input
    video_url = input("Enter the YouTube video URL: ").strip()
    choice = input("Do you want to download video or audio? (v/a): ").strip().lower()

    if choice == 'v':
        download_video(video_url)
    elif choice == 'a':
        download_audio(video_url)
    else:
        print("Invalid choice. Please enter 'v' for video or 'a' for audio.")
