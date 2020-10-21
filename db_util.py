# std lib
from collections import namedtuple
import re
import sqlite3
import tarfile
from typing import Any, Generator, List, TypeVar


match = TypeVar("match", re.match, None)
tarData = TypeVar("tar", tarfile.TarFile, None)
Song = namedtuple("Song", ["artist", "name"])


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
            # decode bytes object coming from tar
            data = tar.extractfile(file_).read().decode("utf-8")
            yield data.split()


def words_in_dict(song: List[str], dict_: List[str]) -> None:
    """Checking how many words from 'song' are in 'dict_'."""
    good_words = []
    bad_words = []

    #normalize with .lower()
    lowered = [word.strip().lower() for word in dict_]
    for word in song:
        if word.lower() in lowered:
            good_words.append(word)
        else:
            bad_words.append(word)
#     print(good_words)
#     print(bad_words)
    good = len(good_words)
    bad = len(bad_words)
#     print("good:", good)
#     print("bad:", bad)
    print("good %: ", round((good/(good+bad))*100))
        
