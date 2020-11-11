from db_util import *
# import types
import sqlite3


db_file = "lyrics.db"


def test_db_connect_returns_cursor_object():
    db, connection = db_connect(db_file)
    assert type(db) == sqlite3.Cursor
    connection.close()


def test_db_connect_returns_connection_object():
    db, connection = db_connect(db_file)
    assert type(connection) == sqlite3.Connection
    connection.close()


def test_open_db_returns_cursor_and_connection_objects():
    db, connection = open_db(db_file)
    assert type(db) == sqlite3.Cursor
    assert type(connection) == sqlite3.Connection
    connection.close()


def test_create_db_returns_cursor_and_connection_objects():
    db, connection = open_db(db_file)
    assert type(db) == sqlite3.Cursor
    assert type(connection) == sqlite3.Connection
    connection.close()


def test_find_record_returns_empty_list_if_not_found():
    result = find_record("notindb", "definitelynotindb")
    assert result.fetchall() == []
