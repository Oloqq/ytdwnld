from pytube import YouTube, Playlist
from downloader import assess_metadata, clear_title
# yt = YouTube('https://www.youtube.com/watch?v=xwCk8H7-DdI')
# res = yt.streams.filter(only_audio=True, file_extension='webm')
# print(res)
# path = res.first().download()
# print(path)

# inp = ffmpeg.input(path)
# out = ffmpeg.output(inp, 'out.mp3')

# fumar_mata = 'https://www.youtube.com/playlist?list=PLks6UYnFddFlchoJnLIOB-gcegojnpAD7'
# yt = Playlist(fumar_mata)
# print(yt)

# links = ['https://www.youtube.com/watch?v=UNMmGAggNUw', 'https://www.youtube.com/watch?v=CBpQXGp5oMs', 'https://www.youtube.com/watch?v=KHuTEryT8ks', 'https://www.youtube.com/watch?v=0QrUuIPPWn4', 'https://www.youtube.com/watch?v=EB8XKCxYPgE', 'https://www.youtube.com/watch?v=xwCk8H7-DdI']
# data = []
# for a in links:
# 	yt = YouTube(a)
# 	yt_title, channel = clear_title(yt.title), yt.author
# 	title, artists = assess_metadata(yt_title, channel)
# 	data.append((yt_title, title, artists, 'bruh.mp3'))

# print(data.__repr__())

data = [('Mataaaaaaaaa - CAMEL', 'CAMEL', 'Mataaaaaaaaa ', 'bruh.mp3'), ('Mata - WHITE MINT', 'WHITE MINT', 'Mata ', 'bruh.mp3'), ('Mata - GOLD', 'GOLD', 'Mata ', 'bruh.mp3'), ('Mata - L&M', 'L&M', 'Mata ', 'bruh.mp3'), ('Mata - LUCKY', 'LUCKY', 'Mata ', 'bruh.mp3'), ('Mata - KLUBOWE', 'KLUBOWE', 'Mata ', 'bruh.mp3'), ('Mata - CAMEL', 'CAMEL', 'Mata ', 'bruh.mp3'), ('Mata - WHITE MINT', 'WHITE MINT', 'Mata ', 'bruh.mp3'), ('Mata - GOLD', 'GOLD', 'Mata ', 'bruh.mp3'), ('Mata - L&M', 'L&M', 'Mata ', 'bruh.mp3'), ('Mata - LUCKY', 'LUCKY', 'Mata ', 'bruh.mp3'), ('Mata - KLUBOWE', 'KLUBOWE', 'Mata ', 'bruh.mp3')]
size = len(data)

i = 0
for d in data:
	i += 1
	print(f'{i:<3} {d[0]:<40} {d[2]:<20} {d[1]:<20} {d[3]}')

# for link in playlist:
# 		i += 1
# 		print(f'{i}/{size}: ', end='') # print progress
		
# 		video_title, status, title, artists, path = download_song(link, subfolder)
# 		metadata_log.write(f'{i}/{size>3}: ')
# 		if status == 'present':
# 			present += 1
# 			new_files.append((path, video_title, title, artists))
# 		elif status == 'downloaded':
# 			downloaded += 1
# 			new_files.append((path, video_title, title, artists))