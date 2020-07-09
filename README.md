# scrabble-comp
Scrabble word list filtering based on list comprehensions

# Word List Filter (Wolf)
Each filter method will return a new wolf so that calls can be chained together.
    ex. wolf(words).len(2).prefix('a').words
        wolf().smaller(3).words

Each filter will keep track of a descripton of the operations performed on the list.
n.b. no ,'s or ;'s are used in the desc, just a space between each condition; it looks
somewhat like set notation.

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

# twl.py
Contains:

    - helper methods for wordlist files
    - a url to TWL 06
    - a method to download the TWL 06
    - letters === string.ascii_lowercase
    - vowels === 'aoeui'
    - notvowels === letters - vowels (__n.b. I didn't want to look up how consonants is spelt, and didn't want to chance leaving a mispelling__)

# use.py

Just a script to set up an interactive sessions.

# lists.py

Generates lists.
