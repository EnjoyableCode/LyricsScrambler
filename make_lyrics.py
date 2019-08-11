'''
make_lyrics.py

usage:

python make_lyrics.py

then enter band and song as prompted to see scrambled lyrics

created by Colin Nicholson (colin.jay.nicholson <at> gmail <dot> com)

makes use of the thesaurus.py Python library created by robert <at> robertism <dot> com

'''


from get_rhymes import get_lyrics, synonize_lyrics
import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    print 'Please enter a band or musician name:'
    band = raw_input()
    print 'Please enter their song name:'
    song = raw_input()
    lyrics = get_lyrics(band,song)
    if lyrics:
        new_data = synonize_lyrics(lyrics)
        print 'Old lyrics:', lyrics
        print 'New lyrics:', new_data
    else:
        print 'Song not found'

