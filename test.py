from pytube import YouTube
yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
res = yt.streams.filter(only_audio=True)
print(res)