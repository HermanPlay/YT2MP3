from pytube import YouTube
import os
  
# url input from user
def download(url: str) -> bytes: 
    cwd = os.getcwd()
    print(cwd)
    yt = YouTube(url)
  
    video = yt.streams.filter(only_audio=True).first()
    
    # download the file
    out_file = video.download(output_path=cwd, filename='audio.mp3')
    print(out_file)
    
    with open(out_file, 'rb') as file:
        audio = file.read()

    return audio


download('https://www.youtube.com/watch?v=0rEPcSfXQgc')