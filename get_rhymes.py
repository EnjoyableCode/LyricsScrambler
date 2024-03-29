'''
get_rhymes.py

library to run make_lyrics.py

created by Colin Nicholson (colin.jay.nicholson <at> gmail <dot> com)

'''

import requests
from bs4 import BeautifulSoup
from random import randint
import sys, os
cwd = os.getcwd()
sys.path.append(cwd + '/thesaurus_api/thesaurus/')
from thesaurus import Word

def rhymes(word):
    """Gets list of rhyming words for a given input word.

    Parameters
    ----------
    String word
    input word to get rhymes for
    
    Returns
    -------
    list wordlist

    list of rhyming words for given input word
    """
    wordlist = []
    r = requests.get('https://www.rhymezone.com/r/rhyme.cgi?Word=' + word + '&typeofrhyme=perfect&org1=syl&org2=l&org3=y', timeout=5)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:    
        data = soup.body.findAll('a')
        get = False
        for d in data:
            if d.text:
                if get:
                    wordlist.append(d.text.strip().replace(u'\xa0', u' '))
                if 'Advanced' in d.text:
                    get = True
                
    except Exception as e:
        print 'error parsing html', e
    return wordlist

thesau_dict = {}
rhyme_dict = {}

def get_random_word():
    """Downloads the data thesaurus.com has for our word.

    Parameters
    ----------
    None
    
    Returns
    -------
    String ran_word

    random synonym of random word in original lyrics
    """
    global thesau_dict
    ran_word = None
   
    inp_words = []
    for word in thesau_dict:
        inp_words.append(word)

    rand_num = randint(0,len(inp_words) - 1)
    ran_inp = inp_words[rand_num]
    synos = thesau_dict[ran_inp]

    if synos:
        rand_num = randint(0,len(synos) - 1)
        ran_word = synos[rand_num]
    
    print 'adding random word:', ran_word
    return ran_word

def get_lyrics(band,song):
    """Downloads the data thesaurus.com has for our word.

    Parameters
    ----------
    String band
    name of band or musician who is credited for the song

    String song 
    name of song whose lyrics we want to scramble
    
    Returns
    -------
    String lyrics

    original song lyrics
    """
    r = requests.get('https://www.azlyrics.com/lyrics/' + band + '/' + song.replace(' ','') + '.html',timeout=5)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.select('div')[10].text

    if song.lower() in data.lower():
        datasplit = data.split('\n')
        songcount = 0
        lyrics = ''
        for d in datasplit:
            if 'if  ( /Android|webOS|iPhone|iPod' in d:
                break
            if songcount > 1:
                lyrics = lyrics + '\n' + d
            if song.lower() in d.lower():
                songcount += 1
        return lyrics

    else:
        return None
    

def synonize_lyrics(lyrics):
    """Downloads the data thesaurus.com has for our word.

    Parameters
    ----------


    String lyrics
    original lyrics for song
    
    Returns
    -------
    String new_lyrics

    newly created version of lyrics with synonyms/rhymes/randomless
    used to alter original song lyrics
    """
    global thesau_dict
    global rhyme_dict
    lyricss = lyrics.split('|||')
    lines = lyrics.split('\n')
    new_lyrics = ''
    last_line_ender = ''
    end_rhyme = False
    
    for line in lines:
        last_line = False
        new_line = ''
        words = line.split(' ')
        
        for index, word in enumerate(words):
            new_word = ''
            if index == len(words) - 99:
                last_line = True
                if last_line_ender:
                    if last_line_ender not in rhyme_dict:
                        rhyme_list = rhymes(last_line_ender)
                        print 'rhyme list is', rhyme_list
                        if rhyme_list:
                            rand_num = randint(0,len(rhyme_list) - 1)
                            new_word = rhyme_list[rand_num]
                            print 'new rhyming word is', new_word
                            last_line_ender = ''
                else:
                    last_line_ender = word
            if not new_word:
                if word not in thesau_dict:
                    synos = Word(word).synonyms()
                    thesau_dict[word] = synos
                else:
                    synos = thesau_dict[word]
                new_word = word
                if synos:
                    print synos
                    rand_num = randint(0,len(synos) - 1)
                    new_word = synos[rand_num]
                else:
                    new_word = get_random_word()
                    if not new_word:
                        new_word = word
            if last_line:
                last_line_ender = new_word
                if end_rhyme:
                    last_line_ender = ''
                    end_rhyme = False
                else:
                    end_rhyme = True
            print 'final word to add:', new_word
            chance = randint(0,1)
            if chance == 0:
                new_line = new_line + ' ' + new_word
            else:
                new_line = new_line + ' ' + word
        new_lyrics = new_lyrics + '\n' + new_line
    return new_lyrics

