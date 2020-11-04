from db_util import *
import types
import sqlite3


words = word_list("/usr/share/dict/web2")
db_file = "lyrics.db"
tar_file = "2.tar.gz"


def test_word_list_returns_list():
    assert type(words) == list


def test_word_list_returns_not_empty():
    assert len(words) > 0


def test_word_list_elements_are_strings():
    assert all(map(lambda x: type(x) == str, words)) == True


def test_open_db_succeeds():
    db, connection = open_db(db_file)
    assert type(db) == sqlite3.Cursor
    assert type(connection) == sqlite3.Connection
    connection.close()


def test_tar_contents_returns_generator():
    assert type(tar_contents(tar_file)) == types.GeneratorType


def test_split_name_returns_list():
    string = "someblock100/someartist_some song.txt"
    assert type(split_name(string)) == list


def test_split_name_has_no_txt_string():
    """The .txt suffix has been removed from the file name."""
    string = "someblock100/someartist_some song.txt"
    assert ".txt" not in split_name(string)[-1]
