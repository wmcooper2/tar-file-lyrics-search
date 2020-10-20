# std lib
from collections import namedtuple
import re
import sqlite3
import tarfile
from typing import Generator, List, TypeVar


match = TypeVar("match", re.match, None)
tarData = TypeVar("tar", tarfile.TarFile, None)
Song = namedtuple("Song", ["artist", "name"])


def open_db(database):
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


def split_name(name: str) -> List[namedtuple]:
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

def simple_word_count(name: str):
    counter = 0

    # need to work around the songs with problem names
    with open("problem_files.txt", "r") as f:
        problems = f.read()
    files = contents(name)
    for file_ in files:
        if file_.endswith(".txt"):
            first_split = file_.rstrip(".txt")
            split_name = first_split.split("_")
            if "Jan & Dean" in first_split:
                print("\nfound it2!", split_name[0])
            if str(first_split) in problems:
                print("\nfound it!", split_name[0])
            counter += 1
            print(f"{counter}", end="\r", flush=True)
