# scrabble words list
import urllib.request as inet
import string

# the site owners ask that you download and cache the file, and not hammer their servers
twl_url = 'https://www.wordgamedictionary.com/twl06/download/twl06.txt'
fname = 'twl06.txt'

letters = string.ascii_lowercase
vowels = 'aoeui'
notvowels = ''.join(c for c in letters if c not in vowels)


def prepOutput(words, end='\n'):
    return [w+end for w in words]


def cleanInput(words):
    "filter for blanks prodced by blank lines; tolower"
    return [w.lower() for w in words if w]


def savetext(words, file):
    with open(file, 'w') as f:
        return f.writelines(prepOutput(words))


def opentext(file):
    with open(file, 'r') as f:
        return cleanInput([w.strip() for w in f.readlines()])


def wgetwordlist(url=twl_url):
    wordfile = inet.urlopen(url)
    wordfile.readline()  # our url starts with 'TWL06 ...' could assert on return value
    return cleanInput([r.decode('utf-8').strip() for r in wordfile])


def dowloadWordlist(url=twl_url, name=fname):
    savetext(wgetwordlist(url), name)


def openlist(file=fname):
    return opentext(file)
