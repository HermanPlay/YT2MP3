from pytube import YouTube # type: ignore 
import os
import time


def fix(title: str) -> None:

    src = title + ".mp3"
    dst = title + ".wav"

    # convert mp3 to wav
    os.system(f"ffmpeg -loglevel quiet -analyzeduration 2147483647 -probesize 2147483647 -i {src} {dst}")

    os.remove(src)

    src = title + ".wav"
    dst = title + ".mp3"

    os.system(f"ffmpeg -loglevel quiet -analyzeduration 2147483647 -probesize 2147483647 -i {src} {dst}")

    os.remove(f"{title}.wav")


# url input from user
def download(url: str) -> str:
    cwd = os.getcwd()
    yt = YouTube(url)
    orig_title = yt.streams[0].title
    title = str(int(time.time()))

    video = yt.streams.filter(only_audio=True).first()

    # download the file
    out_file = video.download(output_path=cwd, filename="audio.mp3") # type: ignore 

    new_file = title + ".mp3"
    os.rename(out_file, new_file)

    try:
        fix(title)
    except Exception as e:
        print(f"Failed converting to wav and mp3 | {e}")

    os.rename(new_file, f"{orig_title}.mp3")
    return orig_title
