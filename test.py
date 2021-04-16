from pytube import YouTube
import ffmpeg
yt = YouTube('https://www.youtube.com/watch?v=xwCk8H7-DdI')
res = yt.streams.filter(only_audio=True, file_extension='webm')
print(res)
path = res.first().download()
print(path)

# inp = ffmpeg.input(path)
# out = ffmpeg.output(inp, 'out.mp3')