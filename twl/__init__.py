# twl init.py
from .wolf import wolf_from_file, Wolf
from .twl import vowels, letters, notvowels, digraphs
from .twl import prepOutput as prep_words

__all__ = [wolf_from_file, Wolf, vowels, letters, notvowels, digraphs, prep_words]
