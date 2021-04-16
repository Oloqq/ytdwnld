# pylint: disable=unused-wildcard-import, method-hidden
# pylint: enable=too-many-lines
from moviepy.editor import *

mp4_file = r'E:\Programming\Python\ytplaylistdownload\YouTube Rewind 2019 For the Record  YouTubeRewind.mp4'
mp3_file = r'E:\Programming\Python\ytplaylistdownload\converted.mp3'

audioclip = AudioFileClip(mp4_file)

audioclip.write_audiofile(mp3_file)

audioclip.close()