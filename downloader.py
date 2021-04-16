# playlist can't be set to private,

# pylint: disable=unused-variable

from pytube import Playlist, YouTube
from moviepy.editor import AudioFileClip
import sys
import os
import re
import eyed3

def one_of_in(one_of, container):
	for a in one_of:
		if a in container:
			return a
	return False

def clear_title(t: str):
	# remove HTML
	t = re.sub(r'(&\w*;)+', '', t)
	
	# remove characters disliked by windows
	t = re.sub(r'[\\/:*?"<>|]+', ' ', t).strip()
	# t = re.sub(r'[^\w\s\-&.()]+', '', t)
	
	return t

def assess_metadata(yt_title, channel):
	feat_marks = ['ft.', 'feat.', 'ft ']
	
	def isolate_feats(raw):
		artists = ''
		found = one_of_in(feat_marks, raw)
		if found != False:
			parts = raw.partition(found)
			# print(parts)
			leftover = parts[0]
			artists = parts[2].strip().replace(', ', ';') + ';'
			return artists, leftover
		else:
			return '', raw
	
	# exceptions (case insensitive)
	dash_artists = ['Jan - rapowanie', 'Jan-rapowanie']
	
	artists = ''
	title = ''
	
	for a in dash_artists:
		pos = yt_title.lower().find(a.lower())
		if pos != -1:
			artists += a + ';'
			yt_title = yt_title[:pos] + yt_title[pos+len(a):]
	
	artist_part = None
	title_part = None
	parts = yt_title.partition('-')
	if parts[1] == '': # no dash
		title_part = yt_title.strip()
		if artists == '': # making sure no artist with a dash was detected
			artists = channel + ';'
	else:
		artist_part = parts[0]
		title_part = parts[2].strip()
		
		feats, artist_part = isolate_feats(artist_part)
		
		pre = artists
		def sep_by(sep):
			artists = ''
			separated = artist_part.split(sep)
			if len(separated) > 1:
				for a in separated:
					if a != '':
						artists += a.strip() + ';'
			return artists
		artists += sep_by(', ')
		artists += sep_by(' x ')
		artists += sep_by(' & ')
		if artists == pre: # no separators
			artists += artist_part
				
		artists += feats
				
	# process title (move feats to artists) (clear prod.)
	title_part = re.sub(r'[(]*prod.*', '', title_part).strip()
	feats, title = isolate_feats(title_part)
	artists += feats
	
	return title, artists
	
	# cool syntax for altering all elements
	# parts = list(title.partition('-'))
	# parts[:] = [p.strip() for p in parts]	

def set_metadata(filename, title, artists):
	tag = eyed3.load(filename).tag
	tag.artist = artists
	tag.title = title
	tag.save()

def ask_about_metadata(filename, yt_title, assessed_title, assessed_artists, tutorial=False):
	if tutorial:
		print('Enter correct values or press ENTER to use assessed ones. (Separate artists with ";")')
	
	print('YT video title:', yt_title)
	inp = input('Assessed title: ' + assessed_title + ' | ')
	if inp != '':
		assessed_title = inp
	inp = input('Assessed artists: ' + assessed_artists.strip(';') + ' | ')
	if inp != '':
		assessed_artists = inp
		
	set_metadata(filename, assessed_title, assessed_artists)

def download_song(yt_link, save_path='', confirm_properties=False):
	yt = YouTube(yt_link)
	yt_title, channel = clear_title(yt.title), yt.author
	mp3_path = os.path.join(save_path, yt_title + '.mp3')
	if os.path.exists(mp3_path):
		print(yt_title, 'is already downloaded. Skipping.')
		tag = eyed3.load(mp3_path).tag
		return (yt_title, 'present', tag.title, tag.artist, mp3_path)
		
	print('Downloading', yt_title)
	mp4_path = yt.streams.filter(only_audio=True).first().download(save_path, filename=yt_title)	
	audio = AudioFileClip(mp4_path)
	audio.write_audiofile(mp3_path)
	audio.close()
	os.remove(mp4_path)
	
	title, artists = assess_metadata(yt_title, channel)
	
	if confirm_properties:
		ask_about_metadata(mp3_path, yt_title, title, artists, tutorial=True)
	else:
		set_metadata(mp3_path, title, artists)
	
	return (yt_title, 'downloaded', title, artists, mp3_path)

def download_playlist(yt_link, save_path=''):
	playlist = Playlist(yt_link)
	size = len(playlist)
	if size == 0:
		print('Failed getting playlist, or playlist is empty. Make sure the playlist is not set to private.')
		return
		
	subfolder = os.path.join(save_path, clear_title(playlist.title))
	
	present = []
	downloaded = []
	
	i = 0
	for link in playlist:
		i += 1
		print(f'{i}/{size}: ', end='') # print progress
		
		video_title, status, title, artists, path = download_song(link, subfolder)
		if status == 'present':
			present.append((video_title, artists, title, path))
		elif status == 'downloaded':
			downloaded.append((video_title, artists, title, path))
			
	with open(subfolder + '/metadata.txt', 'w') as file:
		def save(id, data):
			file.write(f'{id:<3} {data[0]:<40} {data[1]:<20} {data[2]:<20} {data[3]}')
		
		# big brain header writing
		save('ID', ('Video title', 'Assessed artists', 'Assessed title', 'Filename'))
		i = 0
		for d in downloaded:
			i += 1
			save(i, d)
		
		if len(present) > 0:
			file.write('# Entries below were already present, not downloaded; You can still modify their metadata as usual')
			for p in present:
				i += 1
				save(i, p)
	
			
	# print()
	# print('Check new files\' metadata')
	# print('Enter correct values or press ENTER to use assessed ones. (Separate artists with ";")')
	# for entry in new_files:
	# 	tag = eyed3.load(entry[0]).tag
	# 	title = entry[2]
	# 	artists = entry[3]
	# 	print('YT video title:', entry[1])
	# 	inp = input('Assessed title: ' + title + ' ')
	# 	if inp != '':
	# 		title = inp
	# 	inp = input('Assessed artists: ' + artists.strip(';') + ' ')
	# 	if inp != '':
	# 		artists = inp
	# 	tag.artist = artists
	# 	tag.title = title
	# 	tag.save()

if __name__ == '__main__':
	print('YEEEEEEE')
	# video_title, status, title, artists = download_song('https://www.youtube.com/watch?v=XykXStXeVO8', 'test2', confirm_properties=True)
	# print(video_title, status, title, artists)
	dw = 'https://www.youtube.com/playlist?list=PLlBePZw5hmReewZPbnTRJsfNvhAxgryii'
	fumar_mata = 'https://www.youtube.com/playlist?list=PLks6UYnFddFlchoJnLIOB-gcegojnpAD7'
	klubowe = 'https://www.youtube.com/watch?v=xwCk8H7-DdI'
	# download_song(klubowe, save_path='test', confirm_properties=True)
	# download_playlist(dw)
	download_playlist(fumar_mata, 'test2')
	
	