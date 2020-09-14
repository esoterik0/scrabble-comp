# scrabble-comp
Scrabble word list filtering based on list comprehensions

It would seem that I have duplicated some of the functionality of zyzzyva the official tool. (https://scrabbleplayers.org/w/NASPA_Zyzzyva_Download)


# Word list

    TWL06 - there are facilities to dowload this
    NWL18 - this is the current list, but no easy download link

## NWL18

The zyzzyva tool is the official electronic edition of the NWL18; they do not offer a freely accessable .txt copy for download.

One can obtain a .txt copy of this wordlist by:
    - installing zyzzyva
    - open zyzzyva
    - do first time opening database init
    - open a search
    - choose in word list
    - press search; NWL2018 should already be chosen
    - press save as or menu-file->save-as
    - save the word list (default name is nwl18.txt)

I am tempted to host the file on a seperate repository, so that it can stay until it gets DMCA'd, I doubt fair use would count in this case.


# Word List Filter (Wolf)
Each filter method will return a new wolf so that calls can be chained together.

ex.

    wolf(words).len(2).prefix('a').words

        wolf().smaller(3).words

Each filter will keep track of a descripton of the operations performed on the list. n.b. no ,'s or ;'s are used in the desc, just a space between each condition; it looks somewhat like set notation.

## Filters:
    .len                    filters by length
    .lenlst                 filters by lengths set by a list
    .smaller                filters by length <=
    .bigger                 filters by length >=
    .prefix                 filters by prefix
    .starts                     " "
    .postfix                filters by postfix
    .ends                       " "
    .contains               filters for words with the whole string
    .hasltrs                filters for words with all of the letters in ltrs
    .notltrs                filters for words with none of the letters in ltrs
    .foo                    filters for words that return true for foo(word); catch all for fancier stuff
    .vowel_count            filters for words with exactly num vowels
    .vowel_countlst         filters for words with any [num, ...] vowels
    .vowel_count_bigger     filters for words with vowels >= num
    .vowel_count_smaller    filters for words with vowels <= num

## Set operations:
    .union
    .difference
    .intersection

## Utilities:
    .empty                  returns an empty wolf
    .save                   saves list to file
    .getDesc                gets a description of list
    .save_by_letter         spilits the list into lists starting with a letter, and saves each file
    .save_by_last_letter    spilits the list into lists ending with a letter, and saves each file

## wordlist:

The Wolf will:
    - try to load nwl18.txt from local folder, then if it failed
    - try to load twl06.txt from local folder, then if it failed
    - try dowload twl06.txt, and save to local folder then load.
    - if that fails fail; will trow an exception since words is never assigned.

# twl.py
Contains:

    - helper methods for wordlist files
    - a url to TWL 06
    - a method to download the TWL 06
    - letters === string.ascii_lowercase
    - vowels === 'aoeui'
    - notvowels === letters - vowels (__n.b. I didn't want to look up how consonants is spelt, and didn't want to chance leaving a mispelling__)

# use.py

A script to set up an interactive sessions; i.e. use the library interactively.

## helper functions

All the helper functions return a list of lists of words each list is a different lenght starting at 2 and going to the max.

### spell(ltrs, wild=0)

returns words that can be spelled with the letters given with wild wild letters

### starts(fix, ltrs, wild=0)

returns words that start with `fix` and can be spelled with the given letters and wilds

### ends(fix, ltrs, wild=0)

returns words that end with `fix` and can be spelled with the given letters and wilds

### contains(fix, ltrs, wild=0)

returns words that contain `fix` within and can be spelled with the given letters and wilds

# lists.py

Generates lists.

# docs.py

Uses docx to generate .docx documents.
