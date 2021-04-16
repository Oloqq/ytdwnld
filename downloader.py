# playlist can't be set to private,

from pytube import Playlist, YouTube
from moviepy.editor import AudioFileClip
import sys
import os
import re
import eyed3

# fumar mata
# https://www.youtube.com/playlist?list=PLks6UYnFddFlchoJnLIOB-gcegojnpAD7

def one_of_in(one_of, container):
	for a in one_of:
		if a in container:
			return a
	return False

def clear_title(t: str):
	# remove HTML
	t = re.sub(r'(&\w*;)+', '', t)
	
	# remove characters disliked by windows or pytube
	# t = re.sub(r'[^\w\s\-&.()]+', '', t)
	t = re.sub(r'[\\/:*?"<>|]+', ' ', t).strip()
	
	return t

def assess_properties(raw, channel):
	feat_marks = ['ft.', 'feat.']
	
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
		pos = raw.lower().find(a.lower())
		if pos != -1:
			artists += a + ';'
			raw = raw[:pos] + raw[pos+len(a):]
	
	artist_part = None
	title_part = None
	parts = raw.partition('-')
	if parts[1] == '': # no dash
		title_part = raw.strip()
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

def ask_about_metadata(filepath, yt_title, assessed_title, assessed_artists):
	tag = eyed3.load(filepath).tag
	print('Enter correct values or press ENTER to use assessed ones. (Separate artists with ";")')
	print('YT video title:', yt_title)
	inp = input('Assessed title: ' + assessed_title + ' | ')
	if inp != '':
		assessed_title = inp
	inp = input('Assessed artists: ' + assessed_artists.strip(';') + ' | ')
	if inp != '':
		assessed_artists = inp
	tag.artist = assessed_artists
	tag.title = assessed_title
	tag.save()

def download_song(yt_link, save_path='test', confirm_properties=False):
	yt = YouTube(yt_link)
	title, channel = clear_title(yt.title), yt.author
	mp3_path = os.path.join(save_path, title + '.mp3')
	if os.path.exists(mp3_path):
		print(title, 'is already downloaded. Skipping.')
		title_assessed, artists = assess_properties(title, channel)
		return (title, 'present', title_assessed, artists, os.path.join(save_path, title + '.mp3'))
		
	print('Downloading', title)
	mp4_path = yt.streams.filter(only_audio=True).first().download(save_path, filename=title)	
	audio = AudioFileClip(mp4_path)
	audio.write_audiofile(mp3_path)
	audio.close()
	os.remove(mp4_path)
	
	title_assessed, artists = assess_properties(title, channel)
	
	if confirm_properties:
		ask_about_metadata(mp3_path, title, title_assessed, artists)
	
	return (title, 'downloaded', title_assessed, artists, mp3_path)

def download_playlist(yt_link):
	playlist = Playlist(yt_link)
	subfolder = clear_title(playlist.title)
	if len(playlist) == 0:
		print('Failed getting playlist')
		return
		
	present = 0
	downloaded = 0
	new_files = []
		
	for link in playlist:
		video_title, status, title, artists, path = download_song(link, subfolder)
		if status == 'present':
			present += 1
			new_files.append((path, video_title, title, artists))
		elif status == 'downloaded':
			downloaded += 1
			new_files.append((path, video_title, title, artists))
			
	print()
	print('Check new files\' metadata')
	print('Enter correct values or press ENTER to use assessed ones. (Separate artists with ";")')
	for entry in new_files:
		tag = eyed3.load(entry[0]).tag
		title = entry[2]
		artists = entry[3]
		print('YT video title:', entry[1])
		inp = input('Assessed title: ' + title + ' ')
		if inp != '':
			title = inp
		inp = input('Assessed artists: ' + artists.strip(';') + ' ')
		if inp != '':
			artists = inp
		tag.artist = artists
		tag.title = title
		tag.save()

if __name__ == '__main__':
	print('YEEEEEEE')
	# video_title, status, title, artists = download_song('https://www.youtube.com/watch?v=XykXStXeVO8', 'test2', confirm_properties=True)
	# print(video_title, status, title, artists)
	dw = 'https://www.youtube.com/playlist?list=PLlBePZw5hmReewZPbnTRJsfNvhAxgryii'
	fumar_mata = 'https://www.youtube.com/playlist?list=PLks6UYnFddFlchoJnLIOB-gcegojnpAD7'
	klubowe = 'https://www.youtube.com/watch?v=xwCk8H7-DdI'
	download_song(klubowe, confirm_properties=True)
	# download_playlist(dw)
	# download_playlist(fumar_mata)
	
	