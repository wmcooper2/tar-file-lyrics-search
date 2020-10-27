# std lib
from collections import namedtuple
import re
import sqlite3
import string
import tarfile
from typing import Any, Generator, List, Set, TypeVar

# 3rd party
from nltk.stem.porter import *

match = TypeVar("match", re.match, None)
tarData = TypeVar("tar", tarfile.TarFile, None)
Song = namedtuple("Song", ["artist", "name"])
stemmer = PorterStemmer()


def open_db(database: str) -> None:
    connection = sqlite3.connect(database)
    db = connection.cursor()
    try:
        db.execute('''CREATE TABLE songs (artist text, name text)''')
    except sqlite3.OperationalError:
        print("Table already exists. Skipping table creation")
    return db, connection


def contents(file_: tarData) -> Generator[str, None, str]:
    """Make a Generator of the tarfile."""
    with tarfile.open(file_, "r:gz") as tar:
        for thing in tar:
            yield thing.name


def contents2(file_: tarData) -> Generator[str, None, str]:
    """Make a Generator of the tarfile."""
    with tarfile.open(file_, "r:gz") as tar:
        for thing in tar:
            yield thing


def populate_database(name: tarData) -> List[namedtuple]:
    results = []
    counter = 0
    files = contents(name)
    for file_ in files:
        if file_.endswith(".txt"):
            split_name = file_.rstrip(".txt")
            split_name = split_name.split("_")
            if len(split_name) > 2:
                print("\nThere is more than one underscore.")
                print(f"\t{split_name}")
                artist = input("What is the correct artist? : ")
                song_name = input("What is the correct song? : ")
            else:
                artist = split_name[0]
                song_name = split_name[1]
            results.append(Song(artist, song_name))
            counter += 1
            print(f"{counter}", end="\r", flush=True)
    return results


def word_list(name: tarData) -> Generator[List[str], None, None]:
    """Splits words into space delimited units. Yields List."""
    files = contents2(name)
    with tarfile.open(name, "r:gz") as tar:
        for file_ in files:
            data = tar.extractfile(file_).read().decode("utf-8")
            yield data.split()


def load_songs(name: tarData) -> Generator[List[str], None, None]:
    """Splits words into space delimited units. Yields List."""
    files = contents2(name)
    with tarfile.open(name, "r:gz") as tar:
        for file_ in files:
            yield tar.extractfile(file_).read().decode("utf-8")


def words_in_dict(song: List[str], dict_: List[str]) -> None:
    """Checking how many words from 'song' are in 'dict_'."""
    return len([word for word in song if word in dict_])
        

# def reference_dict() -> List[str]:
def reference_dict() -> Set[str]:
    """Load the dictionary on the local machine."""
    dictionary = "/usr/share/dict/web2"
    with open(dictionary, "r") as d:
#         return d.readlines()
        ref_dict = d.readlines()
        ref_dict = [word.lower().strip() for word in ref_dict]
#         print(ref_dict[:10])

#     ref_dict = reference_dict()
#     ref_dict = set(ref_dict)
        return set(ref_dict)
#     set_time = timeit(lambda: "cats" in ref_dict, number=10000)


def remove_all(char: str, list_: List[str]) -> List[str]:
    """Removes all char from list_."""
    while char in list_:
        list_.remove(char)
    return list_


def remove_all_punct(word: str) -> str:
    """Removes all punctuation from word."""
    punct = string.punctuation
    for char in punct:
        word = remove_all(char, list(word))
    return "".join(word)


def remove_all_digits(word: str) -> str:
    """Removes all digits from word."""
    digits = string.digits
    for num in digits:
        word = remove_all(num, list(word))
    return "".join(word)

def remove_all_empty_elements(list_: List[Any]) -> List[Any]:
    """Removes all empty elements from list_."""
    while "" in list_:
        list_.remove("")
    return list_


def normalize_words(words: List[str]) -> List[str]:
    """Normalize all the words."""
    strip = (word.strip() for word in words)
    lower = (word.lower() for word in list(strip))
    no_punct = list(map(remove_all_punct, lower))
    no_digits = list(map(remove_all_digits, no_punct))
    return remove_all_empty_elements(no_digits)


def english_score(list_: Set[str], dict_: Set[str]) -> float:
    """Calculate a score for how much of the song is 'real' English.
    
    - 'Real' English words are found in 'dict_'
    - 'dict_' is /usr/share/dict/web2 (macbook)
    - Returns score from 0 to 100
    """

#     found = sum(1 for word in list_ if word in dict_)
#     return round(found/len(list_), 2)
    found = 0
    good = []
    bad = []

    set_list = set(list_)

    for word in set_list:
        if word in dict_:
            good.append(word)
        else:
            bad.append(word)
    
    for word in bad:
        stemmed = stemmer.stem(word)
        if stemmed in dict_:
            good.append(word)

#     print("good:", good)
    print("bad:", bad)
    return round(len(good)/len(set_list), 2)
