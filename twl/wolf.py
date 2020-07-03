# Wordlist filter
from os.path import exists
from .twl import fname
from .twl import savetext
from .twl import dowloadWordlist
from .twl import openlist


def wolf_from_file(file, desc="fromFile"):
    return Wolf(openlist(file), desc)


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
        .len        filters by length
        .lenst      filters by lengths set by a list
        .smaller    filters by length <=
        .bigger     filters by length >=
        .prefix     filters by prefix
        .starts         " "
        .postfix    filters by postfix
        .ends           " "
        .contains   filters for words with the whole string
        .hasltrs    filters for words with all of the letters in ltrs
        .notltrs    filters for words with none of the letters in ltrs
        .foo        filters for words that return true for foo(word); catch all for fancier stuff

    Set operations:
        .union
        .difference
        .intersection

    Utilities:
        .empty      returns an empty wolf
        .save       saves list to file
        .getDesc    gets a description of list
    """
    def __init__(self, words=None, desc="w|"):
        """
        Wolf():
            Checks if the fname exists and load the file if it exists
            If it doesn't exist, download and save the file from twl.TWL_URL
        """
        if not words:
            if not exists(fname):
                dowloadWordlist()

            words = openlist(fname)

        self.words = words
        self._desc = desc

    def __str__(self):
        "Gives a text description of the filters applied and size of resulting set"
        return "{{{}}}={}".format(self._desc, len(self.words))

    __repr__ = __str__

######################################################################################
# Filters

    def len(self, length):
        "filters by length"
        return Wolf(
            [w for w in self.words if len(w) == length],
            self._descat('len==', length)
        )

    def lenst(self, length):
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
            [w for w in self.words if w in st.lower()],
            self._descat('has_str:', st)
        )

    def hasltrs(self, ltrs):
        "filters for words with all of the letters in ltrs"
        return Wolf(
            [w for w in self.words if all(lt in w for lt in ltrs.lower())],
            self._descat('has_all', ltrs)
        )

    def notltrs(self, ltrs):
        "filters for words with none of the letters in ltrs"
        return Wolf(
            [w for w in self.words if all(lt not in w for lt in ltrs.lower())],
            self._descat('has_none', ltrs)
        )

    def foo(self, foo, dec='desc', pro='func:'):
        "fillters for words that return true for foo(word); catch all for fancier stuff"
        return Wolf(
            [w for w in self.words if foo(w)],
            self._descat(pro, dec)
        )

    # alternate names for these functions
    starts = prefix
    ends = postfix

######################################################################################
# set operations

    def union(self, wolf):
        "computes the union of two wolfs"
        swords = set(self.words)
        swords = swords.union(wolf.words)

        return Wolf(
            list(swords),
            '(({{{}}}) U ({{{}}}))'.format(self._desc, wolf.desc)
        )

    def difference(self, wolf):
        "computes the difference of two wolfs"
        swords = set(self.words)
        swords = swords.difference(wolf.words)

        return Wolf(
            list(swords),
            '(({}) - ({}))'.format(self._desc, wolf.desc)
        )

    def intersection(self, wolf):
        "computes the intersection of two wolfs"
        swords = set(self.words)
        swords = swords.intersection(wolf.words)

        return Wolf(
            list(swords),
            '(({}) ^ ({}))'.format(self._desc, wolf.desc)
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

######################################################################################
# private helpers

    def _descat(self, prompt, data):
        "concatenates the new data into the description"
        return '{} {}{}'.format(self._desc, prompt, data)
