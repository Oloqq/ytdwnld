from ytdwnld import run
from testing.data import playlist_link

line = f"_ playlist {playlist_link} testing/results"

run(line.split())