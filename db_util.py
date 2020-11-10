# std lib
from collections import defaultdict, namedtuple
from pathlib import Path
import re
import sqlite3
import string
import tarfile
from typing import Any, Generator, List, Set, TypeVar

# custom
from file_util import split_name

match = TypeVar("match", re.match, None)
tarData = TypeVar("tar", tarfile.TarFile, None)


def db_connect(database: str) -> Any:
    connection = sqlite3.connect(database)
    db = connection.cursor()
    return db, connection


def create_db(database: str) -> Any:
    if Path(database).exists():
        print("Table already exists. Skipping table creation.")
        return db_connect(database)
    else:
        db, connection = db_connect(database)
        try:
            db.execute('''CREATE TABLE songs (artist text, name text, filePath text)''')
            print("Created table 'Songs' in DB")
            return db, connection
        except sqlite3.OperationalError:
            print("An error occurred trying to create a table in the DB.")


def open_db(database: str) -> Any:
    try:
        connection = sqlite3.connect(database)
        db = connection.cursor()
    except:
        print("Couldn't open DB.")
    return db, connection


def find_record(artist_name: str, song_name: str) -> str:
    """Find the record in the db."""
    db, connection = open_db("lyrics.db")
    return connection.execute(f"SELECT * FROM songs WHERE artist=? AND name=?", (artist_name, song_name))


def add_score_to_db(db: Any, english_score: int, song: str) -> sqlite3.Cursor:
    """Add the english_score to the DB."""
    db, connection = open_db("lyrics.db")
    artist, song = split_name(song)
    artist = re.sub("^block[0-9]{,3}/", "", artist)
    print(f"SEARCH :{english_score} {artist} // {song}")
    connection.execute('''UPDATE songs SET englishScore=? WHERE artist=? AND name=?''', (english_score, artist, song))
    connection.commit()
