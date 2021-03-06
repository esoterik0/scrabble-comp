# Wordlist filter
from os.path import exists
from .twl import fname
from .twl import ftwl
from .twl import savetext
from .twl import dowloadWordlist
from .twl import openlist
from .twl import vowels
from .twl import letters

from functools import reduce
from operator import add


def wolf_from_file(file, desc="fromFile"):
    "returns a new wolf from a file, with optional desc"
    return Wolf(openlist(file), desc)


def _total(st, chars):
    "returns the total occurances of each character in chars"
    return reduce(add, (st.count(c) for c in chars))


def _reduceletters(lttrs):
    """
    Takes: 'studios'
    Returns: {'s':2, 't':1, 'u':1, 'd':1, 'i':1, 'o':1}
    """
    key = {}

    for t in lttrs:
        key.setdefault(t, 0)
        key[t] += 1

    return key


def _checklttrs(lttrs):
    "returns a lambda(word) that returns true if the word contains all the letters in lttrs"
    key = _reduceletters(lttrs)
    return lambda word: all(n == _total(word, t) for t, n in key.items())


def _checkinside(lttrs):
    "returns a lambda(word) that returns true if the word can be spelled with the letters in lttrs"
    key = _reduceletters(lttrs)
    return lambda word: all(key.get(t, 0) >= _total(word, t) for t in word)


def _checkwild(lttrs, wild=1):
    "retruns a function(word) that returns true if the word can be spelled with the letters in lttrs and wild blanks"
    key = _reduceletters(lttrs)

    def foo(word):
        wrd = _reduceletters(word)
        cnts = [max(wrd.get(t, 0)-key.get(t, 0), 0) for t in wrd.keys()]
        return sum(cnts, -wild) == 0

    return foo


class Wolf:
    """
    Word List Filter (Wolf)

    Each filter method will return a new wolf so that calls can be chained together.
        ex. wolf(words).len(2).prefix('a').words
            wolf().smaller(3).words

    Each filter will keep track of a descripton of the operations performed on the list.
    n.b. no ,'s or ;'s are used in the desc, just a space between each condition; it looks
    somewhat like set notation.

    Filters:
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
        .has_all                    " "
        .notltrs                filters for words with none of the letters in ltrs
        .has_none                   " "
        .inside                 filters for words composed of letters in lttrs
        .spell                      " "
        .wild                   filters for words composed of letters in lttrs + wild
        .spellwild                  " "
        .foo                    filters for words that return true for foo(word); catch all for fancier stuff
        .vowel_count            filters for words with exactly num vowels
        .vowel_countlst         filters for words with any [num, ...] vowels
        .vowel_count_bigger     filters for words with vowels >= num
        .vowel_count_smaller    filters for words with vowels <= num

    Set operations:
        .union
        .difference
        .intersection

    Utilities:
        .empty                  returns an empty wolf
        .save                   saves list to file
        .getDesc                gets a description of list
        .save_by_letter         spilits the list into lists starting with a letter, and saves each file
        .save_by_last_letter    spilits the list into lists ending with a letter, and saves each file
        """
    def __init__(self, words=None, desc="w|"):
        """
        Wolf():
            Checks if the fname exists and load the file if it exists
            If it doesn't exist, download and save the file from twl.TWL_URL
        """
        if words is None:  # empty list [] is not none
            if exists(fname):
                words = openlist(fname)
                print('opened ', fname)
            else:
                if not exists(ftwl):
                    dowloadWordlist()

                words = openlist(ftwl)
                print('opened ', ftwl)

        self.words = words
        self._desc = desc

    def __call__(self):
        "the call operator returns words"
        return self.words

    def __str__(self):
        "Gives a text description of the filters applied and size of resulting set"
        return "{{{}}}={}".format(self._desc, len(self.words))

    __repr__ = __str__

    def __len__(self):
        return len(self.words)

######################################################################################
# Filters

    def len(self, length):
        "filters by length"
        return Wolf(
            [w for w in self.words if len(w) == length],
            self._descat('len==', length)
        )

    def lenlst(self, length):
        "filters by lengths set by a list"
        return Wolf(
            [w for w in self.words if len(w) in length],
            self._descat('len==', length)
        )

    def smaller(self, length):
        "filters by length <="
        return Wolf(
            [w for w in self.words if len(w) <= length],
            self._descat('len<=', length)
        )

    def bigger(self, length):
        "filters by length >="
        return Wolf(
            [w for w in self.words if len(w) >= length],
            self._descat('len>=', length)
        )

    def prefix(self, start):
        "filters by prefix"
        return Wolf(
            [w for w in self.words if w.startswith(start.lower())],
            self._descat('start:', start)
            )

    def postfix(self, end):
        "filters by postfix"
        return Wolf(
            [w for w in self.words if w.endswith(end.lower())],
            self._descat('ends:', end)
        )

    def contains(self, st):
        "filters for words with the whole string"
        return Wolf(
            [w for w in self.words if st.lower() in w],
            self._descat('has_str:', st)
        )

    def notltrs(self, ltrs):
        "filters for words with none of the letters in ltrs"
        return Wolf(
            [w for w in self.words if all(lt not in w for lt in ltrs.lower())],
            self._descat('has_none', ltrs)
        )

    def vowel_count(self, num):
        "filters for words with exactly num vowels"
        return Wolf(
            [w for w in self.words if _total(w, vowels) == num],
            self._descat('vowel=', num)
        )

    def vowel_countlst(self, nums):
        "filters for words with any [num, ...] vowels"
        return Wolf(
            [w for w in self.words if _total(w, vowels) in nums],
            self._descat('vowel=', nums)
        )

    def vowel_count_bigger(self, num):
        "filters for words with vowels >= num"
        return Wolf(
            [w for w in self.words if _total(w, vowels) >= num],
            self._descat('vowel>=', num)
        )

    def vowel_count_smaller(self, num):
        "filters for words with vowels <= num"
        return Wolf(
            [w for w in self.words if _total(w, vowels) <= num],
            self._descat('vowel<=', num)
        )

    def foo(self, foo, dec='desc', pro='func:'):
        "fillters for words that return true for foo(word); catch all for fancier stuff"
        return Wolf(
            [w for w in self.words if foo(w)],
            self._descat(pro, dec)
        )

    def hasltrs(self, ltrs):
        "filters for words with all of the letters in ltrs"
        return self.foo(_checklttrs(ltrs.lower()), ltrs, 'has_all:')

    def inside(self, lttrs):
        "filters for words composed of letters in lttrs"
        return self.foo(_checkinside(lttrs.lower()), lttrs, 'inside:')

    def wild(self, lttrs, wild=1):
        "filters for words composed of letters in lttrs + wild"
        return self.foo(_checkwild(lttrs.lower(), wild), lttrs, 'inside+{}:'.format(wild))

    # alternate names for these functions

    has_all = hasltrs
    has_none = notltrs
    starts = prefix
    ends = postfix
    spell = inside
    spellwild = wild

######################################################################################
# set operations

    def union(self, wolf):
        "computes the union of two wolfs"
        swords = set(self.words)
        swords = swords.union(wolf.words)

        return Wolf(
            list(swords),
            '({{{}}} U {{{}}})'.format(self._desc, wolf.desc)
        )

    def difference(self, wolf):
        "computes the difference of two wolfs"
        swords = set(self.words)
        swords = swords.difference(wolf.words)

        return Wolf(
            list(swords),
            '({{{}}} - {{{}}})'.format(self._desc, wolf.desc)
        )

    def intersection(self, wolf):
        "computes the intersection of two wolfs"
        swords = set(self.words)
        swords = swords.intersection(wolf.words)

        return Wolf(
            list(swords),
            '({{{}}} ^ {{{}}})'.format(self._desc, wolf.desc)
        )

######################################################################################
# utility/helpers

    getDesc = __str__

    def empty(self):
        "returns the empty set; may not be needed, could be used for comparisons; but size testing would be easier"
        return Wolf([], "empty")

    def save(self, sfname):
        "save the current wordlist to a file"
        savetext(self.words, sfname)

        return self

    def save_by_letter(self, basename, fmt='{}_{}.txt'):
        "spilits the list into lists starting with a letter, and saves each file"
        for wolf, name in [(self.starts(c), fmt.format(basename, c)) for c in letters]:
            wolf.save(name)

    def save_by_last_letter(self, basename, fmt='{}_-{}.txt'):
        "spilits the list into lists ending with a letter, and saves each file"
        for wolf, name in [(self.ends(c), fmt.format(basename, c)) for c in letters]:
            wolf.save(name)

######################################################################################
# private helpers

    def _descat(self, prompt, data):
        "concatenates the new data into the description"
        return '{} {}{}'.format(self._desc, prompt, data)
