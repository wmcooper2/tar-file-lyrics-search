# std lib
from collections import defaultdict, namedtuple
import re
import sqlite3
import string
import tarfile
from typing import Any, Generator, List, Set, TypeVar

# 3rd party
from nltk.stem.porter import *

match = TypeVar("match", re.match, None)
tarData = TypeVar("tar", tarfile.TarFile, None)
Song = namedtuple("Song", ["artist", "name", "filePath"])
stemmer = PorterStemmer()


def create_db(database: str) -> None:
    connection = sqlite3.connect(database)
    db = connection.cursor()
    try:
        db.execute('''CREATE TABLE songs (artist text, name text, filePath text)''')
    except sqlite3.OperationalError:
        print("Table already exists. Skipping table creation")
    return db, connection


def open_db(database: str) -> None:
    try:
        connection = sqlite3.connect(database)
        db = connection.cursor()
    except:
        print("Couldn't open DB.")
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


def split_name(file_name: str) -> List[str]:
    """Separate the artist name from the song name."""
#     split_name = file_name.rstrip(".txt")
    split_name = re.sub(".txt", "", file_name)
    return split_name.split("_")



def populate_database(name: tarData) -> List[namedtuple]:
    """Add artist, song name and file path to DB."""
    results = []
    counter = 0
    files = contents(name)
    for file_ in files:
        if file_.endswith(".txt"):
            artist_song = split_name(file_)
#             artist_song = file_.rstrip(".txt")
#             artist_song = artist_song.split("_")
            if len(artist_song) > 2:
                print("\nThere is more than one underscore.")
                artist = input("What is the correct artist? : ")
                song_name = input("What is the correct song? : ")
            else:
                artist = artist_song[0].strip()
                artist = re.sub("^block\d{,3}/", "", artist)
                song_name = artist_song[1].strip()
            entry = Song(artist, song_name, file_)
            results.append(entry)
            counter += 1
            print(f"{counter}", end="\r", flush=True)
    return results


def lazy_word_list(name: tarData) -> Generator[List[str], None, None]:
    """Splits words into space delimited units. Yields List."""
    files = contents2(name)
    with tarfile.open(name, "r:gz") as tar:
        for file_ in files:
            data = tar.extractfile(file_).read().decode("utf-8")
            yield data.split()


def load_songs(name: tarData) -> [Generator[List[str], None, None], str]:
    """Create generator of songs and file names."""
    files = contents2(name)
    with tarfile.open(name, "r:gz") as tar:
        for file_ in files:
            # dirs in archive returned as None
            extracted = tar.extractfile(file_)
            if extracted is None:
                continue
            else: 
                result = extracted.read().decode("utf-8")
                yield result, file_.name  # gen, TarInfo.name


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


def word_list(list_: str) -> List[str]:
    """Load word list."""
    with open(list_, "r") as f:
        return f.readlines()


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


def english_score(found: int, not_found: int) -> float:
    """Calculate a ratio of how many words were found."""
    return round(found / (found + not_found), 2)


def find_record(artist_name: str, song_name: str) -> str:
    """Find the record in the db."""
    db, connection = open_db("lyrics.db")
    return connection.execute(f"SELECT * FROM songs WHERE artist=? AND name=?", (artist_name, song_name))


def add_score_to_db(db: Any, english_score: int, song: str) -> sqlite3.Cursor:
    """Add the english_score to the DB."""
    db, connection = open_db("lyrics.db")
    artist, song = split_name(song)
    artist = re.sub("^block\d{,3}/", "", artist)
    print(f"SEARCH :{english_score} {artist} // {song}")
    connection.execute('''UPDATE songs SET englishScore=? WHERE artist=? AND name=?''', (english_score, artist, song))
    connection.commit()
