# std lib
from collections import namedtuple
import re
import tarfile
from typing import Generator, List, Set, TypeVar

# 3rd party
# from nltk.stem.porter import *
from nltk.stem.porter import PorterStemmer

# custom
from file_util import (
    remove_all_punct,
    remove_all_digits,
    remove_all_empty_elements,
    tar_contents,
    word_list)


tarData = TypeVar("tar", tarfile.TarFile, None)
match = TypeVar("match", re.match, None)
Song = namedtuple("Song", ["artist", "name", "filePath"])


stemmer = PorterStemmer()


def save_word_list(file_: str, words: Set[str]) -> None:
    """Save word list as text file."""
    with open(file_, "w+") as f:
        for word in words:
            f.write(f"{word}\n")


def word_set(dict_: str) -> Set[str]:
    """Return a normalized set of words from the 'dict_'."""
    dict_ = word_list(dict_)
    dict_ = [word.lower().strip() for word in dict_]
    return set(dict_)


def words_in_dict(list_: Set[str], dict_: Set[str]) -> [Set[str], Set[str]]:
    """Determine which words from list_ are in dict_."""
    not_found = set()
    found = set()
    for word in list_:
        if word in dict_:
            found.add(word) 
        else:
            not_found.add(word)
    #Try to find stemmed words not found in first pass
    for word in not_found.copy():
        stemmed = stemmer.stem(word)
        if stemmed in dict_:
            found.add(word)
            not_found.remove(word)
    return found, not_found


def normalize_words(words: List[str]) -> List[str]:
    """Normalize all the words."""
    strip = (word.strip() for word in words)
    lower = (word.lower() for word in list(strip))
    no_punct = list(map(remove_all_punct, lower))
    no_digits = list(map(remove_all_digits, no_punct))
    return remove_all_empty_elements(no_digits)


def calculate_english_score(song: str, ref_dict: Set[str]) -> int:
    """Calculate a score based on how many English words were found."""
    normalized = normalize_words(song[0].split())
    found, not_found = words_in_dict(normalized, ref_dict)  # sets
    amt_found = len(found)
    amt_not_found = len(not_found)
    score = round(amt_found / (amt_found + amt_not_found), 2)
    return int(score * 100)


def load_songs(name: tarData) -> [Generator[List[str], None, None], str]:
    """Create generator of songs and file names."""
    files = tar_contents(name)
    with tarfile.open(name, "r:gz") as tar:
        for file_ in files:
            # dirs in archive returned as None
            extracted = tar.extractfile(file_)
            if extracted is None:
                continue
            else: 
                result = extracted.read().decode("utf-8")
                yield result, file_.name  # gen, TarInfo.name
