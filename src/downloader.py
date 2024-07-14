import logging
import os
import time

from config.exceptions import FileTooLarge
from pytubefix import YouTube

_logger = logging.getLogger(__name__)


def str_to_ascii(s: str) -> str:
    """
    Function converts string to ascii characters

    :param s: String to convert
    :return: Converted string
    """

    return "".join(i if ord(i) < 128 else " " for i in s)


def fix(title: str) -> None:
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


# url input from user
def download(url: str) -> str:
    """
    Function takes url and downloades video.
    It also calls fix function before return.

    :param url: YouTube video url
    :return: Name of the downloaded file

    :raises: FileTooLarge if file exceeds telegram max upload file size
    """

    yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    ys = yt.streams.get_audio_only()
    orig_title = yt.title
    max_filename_length = 120
    if len(orig_title) > max_filename_length:
        orig_title = orig_title[:120]

    orig_title = str_to_ascii(orig_title)
    orig_title = orig_title.replace("/", "")
    title = str(int(time.time()))

    out_file = ys.download(mp3=True, filename=title)
    try:
        fix(title)
    except Exception as e:
        print(f"Failed converting to wav and mp3 | {e}")

    os.rename(out_file, orig_title + ".mp3")

    file_size = os.path.getsize(orig_title + ".mp3")
    max_file_size = 50 * 1000 * 1000  # 50 MB
    if file_size > max_file_size:
        raise FileTooLarge("The file is too large to send via telegaram bot")
    return orig_title
