# YouTube Downloader

This is a simple Python application to download videos or audio from YouTube using the `yt-dlp` library. The program 
allows users to choose between downloading the best-quality video or an M4A audio file extracted from the video.

## Features
- Download select videos quality or download the best available quality.
- Download audio-only in M4A format with 192kbps quality.
- Automatically handles SSL certificate issues.
- Creates a `downloads` folder to save the downloaded files.

## Requirements
- Python 3.7+
- `yt-dlp` library
- `ffmpeg` (required for audio extraction and conversion)

## Installation
1. Clone this repository or download the script file:
   ```bash
   git clone https://github.com/suminv/yt-download
   cd yt-download
   ```

2. Install the required Python packages:
   ```bash
   pip install yt-dlp
   ```

3. Install `ffmpeg` (if not already installed):
   ```bash
   brew install ffmpeg  # macOS
   sudo apt install ffmpeg  # Linux
   choco install ffmpeg  # Windows (via Chocolatey)
   ```

## Usage
1. Run the script:
   ```bash
   python main.py
   ```

2. Enter the YouTube video URL when prompted.

3. Choose whether to download:
   - Video: Type `ps`
   - Audio: Type `a`
   - Subtitles: Type `s`

4. The downloaded file will be saved in the `downloads` folder.

## Example
### Downloading a Video
```bash
Enter the YouTube video URL: https://www.youtube.com/watch?v=example
Do you want to download video or audio? (v/a): v
```

### Downloading Audio
```bash
Enter the YouTube video URL: https://www.youtube.com/watch?v=example
Do you want to download video or audio? (v/a): a
```

## Troubleshooting
- **SSL Certificate Errors**: The script is configured to bypass SSL verification to avoid certificate errors. Ensure you have Python's `certifi` package installed and updated:
  ```bash
  pip install --upgrade certifi
  ```

- **Missing `ffmpeg`**: Make sure `ffmpeg` is installed and available in your system's PATH.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
