'''
get_rhymes.py

library to get whymes for a given word

created by Colin Nicholson (colin.jay.nicholson <at> gmail <dot> com)

'''

import requests
from bs4 import BeautifulSoup

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
    r = requests.get('https://www.rhymezone.com/r/rhyme.cgi?Word=' + word + '&typeofrhyme=perfect&org1=syl&org2=l&org3=y')
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

