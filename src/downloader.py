import os
from pathlib import Path
import time
import yt_dlp

from config.exceptions import FileTooLarge
from pydantic import BaseModel
from utils import get_logger


_logger = get_logger(__name__)


def str_to_ascii(s: str) -> str:
    """
    Function converts string to ascii characters

    :param s: String to convert
    :return: Converted string
    """

    return "".join(i if ord(i) < 128 else " " for i in s)


def _fix(title: str) -> None:
    """
    Function takes file name and fixes its metadata,
    by converting to wav and back to mp3

    :param title: File name
    """

    src = title + ".mp3"
    dst = title + ".wav"

    # convert mp3 to wav
    os.system(
        f"ffmpeg -loglevel quiet -analyzeduration 2147483647 -probesize 2147483647 -i {src} {dst}"  # noqa E501
    )

    os.remove(src)

    src = title + ".wav"
    dst = title + ".mp3"
    # convert wav to mp3
    os.system(
        f"ffmpeg -loglevel quiet -analyzeduration 2147483647 -probesize 2147483647 -i {src} {dst}"  # noqa E501
    )

    os.remove(f"{title}.wav")


class DownloadResult(BaseModel):
    file_name: str
    file_path: str
    title: str

def download(url: str) -> DownloadResult:
    """
    Function takes a URL and downloads the video as audio.
    It also calls fix function before return.

    :param url: YouTube video URL
    :return: Name of the downloaded file

    :raises: FileTooLarge if file exceeds Telegram's max upload file size
    """
    _logger.info(f"Downloading video from {url=}")

    # yt-dlp options
    max_file_size = 2 * 1024 * 1024 * 1024  # 2 GB (Telegram max file size for uploads)
    file_name = str(int(time.time()))  # Unique file name based on timestamp
    output_template = f"{file_name}.%(ext)s"  # Output file name template
    max_filename_length = 120

    def progress_hook(d):
        """Check file size during download."""
        if d['status'] == 'downloading' and d.get('total_bytes', 0) > max_file_size:
            raise FileTooLarge(f"File exceeds Telegram's max upload size: {d['total_bytes']} bytes")

    ydl_opts = {
        'format': 'bestaudio/best',  # Best audio quality
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_template,  # Output file name
        'progress_hooks': [progress_hook],  # Hook to monitor progress
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            orig_title = info.get('title', 'Unknown Title')
    except FileTooLarge as e:
        _logger.error(f"File too large: {e}")
        raise
    except Exception as e:
        _logger.error(f"Error downloading video: {e}")
        raise

    # Process title
    if len(orig_title) > max_filename_length:
        orig_title = orig_title[:max_filename_length]
    orig_title = str_to_ascii(orig_title).replace("/", "")

    # Find downloaded file path
    out_file = Path(f"{file_name}.mp3").resolve()
    _logger.info(f"Downloaded video to {out_file}")

    result = DownloadResult(file_name=file_name, file_path=str(out_file), title=orig_title)
    return result

def fix_metadata(file_name: str, file_path: str) -> str:
    try:
        _logger.debug(f"Converting {file_path} to wav and mp3")
        _fix(file_name)
    except Exception as e:
        _logger.error(f"Failed converting to wav and mp3 | {e}")
        os.remove(file_path)
        raise e

    file_size = os.path.getsize(file_path)
    max_file_size = 50 * 1000 * 1000  # 50 MB
    if file_size > max_file_size:
        raise FileTooLarge("The file is too large to send via telegaram bot")
    return file_name
