import os
import time

from config.exceptions import FileTooLarge
from pydantic import BaseModel
from pytubefix import YouTube
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


# url input from user
def download(url: str) -> DownloadResult:
    """
    Function takes url and downloades video.
    It also calls fix function before return.

    :param url: YouTube video url
    :return: Name of the downloaded file

    :raises: FileTooLarge if file exceeds telegram max upload file size
    """

    _logger.info(f"Downloading video from {url=}")
    # yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    yt = YouTube(url)

    ys = yt.streams.get_audio_only()
    orig_title = yt.title
    max_filename_length = 120
    if len(orig_title) > max_filename_length:
        orig_title = orig_title[:120]

    orig_title = str_to_ascii(orig_title)
    orig_title = orig_title.replace("/", "")
    file_name = str(int(time.time()))

    out_file = ys.download(mp3=True, filename=file_name)
    _logger.info(f"Downloaded video to {out_file}")
    result = DownloadResult(file_name=file_name, file_path=out_file, title=orig_title)
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
