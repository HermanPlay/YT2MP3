# from pytube import YouTube
from pytubefix import YouTube
import os
import time


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
        f"ffmpeg -loglevel quiet -analyzeduration 2147483647 -probesize 2147483647 -i {src} {dst}"
    )

    os.remove(src)

    src = title + ".wav"
    dst = title + ".mp3"
    # convert wav to mp3
    os.system(
        f"ffmpeg -loglevel quiet -analyzeduration 2147483647 -probesize 2147483647 -i {src} {dst}"
    )

    os.remove(f"{title}.wav")


# url input from user
def download(url: str) -> str:
    """
    Function takes url and downloades video.
    It also calls fix function before return.

    :param url: YouTube video url
    :return: Name of the downloaded file
    """

    yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    ys = yt.streams.get_audio_only()
    orig_title = yt.title
    orig_title = orig_title.replace("/", "")
    title = str(int(time.time()))

    new_file = title + ".mp3"
    out_file = ys.download(mp3=True)
    os.rename(out_file, new_file)

    try:
        fix(title)
    except Exception as e:
        print(f"Failed converting to wav and mp3 | {e}")

    os.rename(new_file, orig_title + ".mp3")
    return orig_title
