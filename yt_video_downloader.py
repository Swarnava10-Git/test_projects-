from tqdm import tqdm, trange
from pytube import YouTube

url = str(input('''YouTube Video Download
Paste your video link here : '''))
yt = YouTube(url)
stream = yt.streams.get_highest_resolution()
stream.download()

for url in tqdm(range(1)):
    tqdm()
print('Successfully Downloaded')
a = str(input(''))