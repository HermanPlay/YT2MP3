from pytube import YouTube
import os
from pydub import AudioSegment


def fix(title: str) -> None:

    src = title + ".mp3"
    dst = title + ".wav"

    # convert mp3 to wav
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")

    os.remove(f"{title}.mp3")

    src = title + ".wav"
    dst = title + ".mp3"

    # convert wav to mp3
    sound = AudioSegment.from_file(src, format="wav")
    sound.export(dst, format="mp3")


# url input from user
def download(url: str) -> str:
    cwd = os.getcwd()
    print(cwd)
    yt = YouTube(url)
    title: str = yt.streams[0].title

    video = yt.streams.filter(only_audio=True).first()

    # download the file
    out_file = video.download(output_path=cwd, filename="audio.mp3")
    print("Downloaded file, processing forward!")

    new_file = title + ".mp3"
    os.rename(out_file, new_file)

    fix(title)

    return title
