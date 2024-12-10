import unittest
import os
from unittest.mock import patch, MagicMock
import tempfile
import io
import sys

from main import (
    is_valid_youtube_url,
    select_resolution,
    download_items,
    download_audio,
    list_available_formats
)


class TestYouTubeDownloader(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for downloads
        self.test_download_dir = tempfile.mkdtemp()

    def test_is_valid_youtube_url(self):
        # Test valid YouTube URLs
        valid_urls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'http://youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtu.be/dQw4w9WgXcQ',
            'youtube.com/watch?v=dQw4w9WgXcQ',
            'www.youtube.com/embed/dQw4w9WgXcQ'
        ]

        # Test invalid YouTube URLs
        invalid_urls = [
            'https://www.google.com',
            'invalid url',
            'https://vimeo.com/123456',
            ''
        ]

        # Check valid URLs
        for url in valid_urls:
            self.assertTrue(is_valid_youtube_url(url), f"Failed for valid URL: {url}")

        # Check invalid URLs
        for url in invalid_urls:
            self.assertFalse(is_valid_youtube_url(url), f"Failed for invalid URL: {url}")

    def test_select_resolution(self):
        # Test resolution selection with mocked input
        test_cases = [
            ('1', 'bestvideo[height<=1080]+bestaudio/best'),
            ('2', 'bestvideo[height<=720]+bestaudio/best'),
            ('3', 'bestvideo[height<=480]+bestaudio/best'),
            ('4', 'bestvideo+bestaudio/best'),
            ('5', 'best')  # Default case
        ]

        for input_val, expected_output in test_cases:
            with patch('builtins.input', return_value=input_val):
                result = select_resolution()
                self.assertEqual(result, expected_output)

    @patch('yt_dlp.YoutubeDL')
    def test_download_items(self, mock_ydl):
        # Mock successful download
        mock_instance = MagicMock()
        mock_ydl.return_value.__enter__.return_value = mock_instance

        # Test single video download
        with patch('builtins.input', return_value='4'):
            download_items('https://www.youtube.com/watch?v=dQw4w9WgXcQ', self.test_download_dir)

        # Verify download method was called
        mock_instance.download.assert_called_once()

    @patch('yt_dlp.YoutubeDL')
    def test_download_audio(self, mock_ydl):
        # Mock successful audio download
        mock_instance = MagicMock()
        mock_ydl.return_value.__enter__.return_value = mock_instance

        download_audio('https://www.youtube.com/watch?v=dQw4w9WgXcQ', self.test_download_dir)

        # Verify download method was called
        mock_instance.download.assert_called_once()

    @patch('yt_dlp.YoutubeDL')
    def test_list_available_formats(self, mock_ydl):
        # Mock format listing
        mock_info_dict = {
            'formats': [
                {'format_id': '22', 'resolution': '720p', 'ext': 'mp4'},
                {'format_id': '18', 'resolution': '360p', 'ext': 'mp4'}
            ]
        }
        mock_ydl.return_value.__enter__.return_value.extract_info.return_value = mock_info_dict

        # Capture stdout

        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the function
        list_available_formats('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Check output
        output = captured_output.getvalue()
        self.assertIn('Format Code: 22', output)
        self.assertIn('Format Code: 18', output)

    def test_invalid_url_handling(self):
        # Test download functions with invalid URL
        with patch('builtins.print') as mock_print:
            download_items('invalid_url', self.test_download_dir)
            mock_print.assert_called_with('Invalid YouTube URL. Please check the link')

        with patch('builtins.print') as mock_print:
            download_audio('invalid_url', self.test_download_dir)
            mock_print.assert_called_with('Invalid YouTube URL. Please check the link')

    def test_download_directory_creation(self):
        # Ensure download directory is created
        test_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

        with patch('yt_dlp.YoutubeDL'), patch('builtins.input', return_value='4'):
            download_items(test_url, self.test_download_dir)

        self.assertTrue(os.path.exists(self.test_download_dir))
        self.assertTrue(os.path.isdir(self.test_download_dir))


if __name__ == '__main__':
    unittest.main()
