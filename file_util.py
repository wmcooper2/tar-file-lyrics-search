# std lib
from collections import namedtuple
import re
import string
import tarfile
from typing import Any, Generator, List, TypeVar


tarData = TypeVar("tar", tarfile.TarFile, None)
match = TypeVar("match", re.match, None)
Song = namedtuple("Song", ["artist", "name", "filePath"])


def tar_contents(file_: tarData) -> Generator[str, None, str]:
    """Make a Generator of the tarfile."""
    with tarfile.open(file_, "r:gz") as tar:
        for thing in tar:
            yield thing


def split_name(file_name: str) -> List[str]:
    """Separate the artist name from the song name."""
    name = re.sub(".txt", "", file_name)
    return name.split("_")


#TODO, continue writing tests from here
def get_file_info(name: tarData) -> List[namedtuple]:
    """Add artist, song name and file path to DB."""
    results = []
    counter = 0
    files = tar_contents(name)
    for file_ in files:
        if file_.name.endswith(".txt"):
            artist_song = split_name(file_.name)
            if len(artist_song) > 2:
                print("\nThere is more than one underscore.")
                artist = input("What is the correct artist? : ")
                song_name = input("What is the correct song? : ")
            else:
                artist = artist_song[0].strip()
                artist = re.sub("^block[0-9]{,3}/", "", artist)
                song_name = artist_song[1].strip()
            entry = Song(artist, song_name, file_.name)
            results.append(entry)
            counter += 1
            print(f"Files parsed: {counter}", end="\r", flush=True)
    print("\n")
    return results


def lazy_word_list(name: tarData) -> Generator[List[str], None, None]:
    """Splits words into space delimited units. Yields List."""
    files = tar_contents(name)
    with tarfile.open(name, "r:gz") as tar:
        for file_ in files:
            data = tar.extractfile(file_).read().decode("utf-8")
            yield data.split()


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


def word_list(list_: str) -> List[str]:
    """Load word list."""
    with open(list_, "r") as f:
        return f.readlines()


def contents(file_: tarData) -> Generator[str, None, str]:
    """Make a Generator of the tarfile."""
    with tarfile.open(file_, "r:gz") as tar:
        for thing in tar:
            yield thing.name


def extract_file_contents(file_name: str, name: tarData) -> bytes:
    """Get the archived file's contents."""
    with tarfile.open(name) as tar:
        data = tar.extractfile(file_name)
        return data.read().decode("utf-8")


def search(pattern: str, file_: str) -> match:
    matches = 0
    counter = 0
    with tarfile.open(name=file_, mode="r") as tar:
        for file_ in tar:
            t = tar.getmember(file_.name)
            if t.isfile():
                try:
                    contents = extract_file_contents(t, file_)
                    res = re.search(pattern, str(contents))
                    if res != None:
                        print(f"{matches}/{counter}: {res}", end="\r", flush=True)
                        matches += 1
                    else:
                        print(f"{matches}/{counter}", end="\r", flush=True)
                except AttributeError:
                    print("Error: ", file_)
                except KeyboardInterrupt:
                    print("Manually quit.")
                    break

            #For testing
            if counter > 2:
                break
            counter += 1
