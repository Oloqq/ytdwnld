import eyed3

file = eyed3.load('aarfw.webm')
tag = file.tag

tag.artist = 'skibidi bap mm dada'
tag.title = 'spotiprosze'

tag.save()

# import eyed3

# audiofile = eyed3.load("song.mp3")
# audiofile.tag.artist = "Token Entry"
# audiofile.tag.album = "Free For All Comp LP"
# audiofile.tag.album_artist = "Various Artists"
# audiofile.tag.title = "The Edge"
# audiofile.tag.track_num = 3

# audiofile.tag.save()

# save proposed metadata to a file with indexes
# allow changing by index