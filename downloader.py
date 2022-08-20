from pytube import YouTube
import os
  
# url input from user
def download(url: str) -> bytes: 
    cwd = os.getcwd()
    print(cwd)
    yt = YouTube(url)
    title = yt.streams[0].title
  
    video = yt.streams.filter(only_audio=True).first()
    
    # download the file
    out_file = video.download(output_path=cwd, filename='audio.mp3')
    print('Downloaded file, processing forward!')
    
    new_file = title + '.mp3'
    os.rename(out_file, new_file)

    return title