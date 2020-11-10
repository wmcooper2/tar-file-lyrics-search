# std lib
from typing import Set

# 3rd party
from nltk.stem.porter import *

# custom
from db_util import word_list
from file_util import tar_contents


stemmer = PorterStemmer()


def save_word_list(file_: str, words: Set[str]) -> None:
    """Save word list as text file."""
    with open(file_, "w+") as f:
        for word in words:
            f.write(f"{word}\n")


def word_set(dict_: str) -> Set[str]:
    """Return a normalized set of words from the 'dict_'."""
    ref_dict = word_list(dict_)
    ref_dict = [word.lower().strip() for word in ref_dict]
    ref_dict = set(ref_dict)


def words_in_dict(list_: Set[str], dict_: Set[str]) -> [Set[str], Set[str]]:
    """Determine which words are and are not in dict_."""
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


def english_score(found: int, not_found: int) -> float:
    """Calculate a ratio of how many words were found."""
    return round(found / (found + not_found), 2)


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
