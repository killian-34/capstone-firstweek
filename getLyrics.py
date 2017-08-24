from PyLyrics import *
import sys

def main2():
    artist = str(sys.argv[1])
    songTitle = str(sys.argv[2])
    lyrics = PyLyrics.getLyrics(artist, songTitle)
    print lyrics

if __name__ == "__main__":
    main2()