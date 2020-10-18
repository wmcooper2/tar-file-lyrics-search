import re
import tarfile
from typing import Generator, TypeVar

match = TypeVar("match", re.match, None)
tarData = TypeVar("tar", tarfile.TarFile, None)


def contents(file_: tarData) -> Generator[str, None, str]:
    """Make a Generator of the tarfile."""
    with tarfile.open(file_, "r:gz") as tar:
        for thing in tar:
            yield thing.name


def extract_file_contents(file_name: str) -> bytes:
    """Get the archived file's contents."""
    with tarfile.open("lyrics.tar.gz") as tar:
        data = tar.extractfile(file_name)
        return data.read().decode("utf-8")


counter = 0
with tarfile.open("lyrics.tar.gz") as tar:
    for file_ in tar:
        t = tar.getmember(file_.name)
        if t.isfile():
            try:
                contents = extract_file_contents(t)
                res = re.search("what is", str(contents))
                if res != None:
                    print(f"{counter}: {res}", end="\r")
                else:
                    print(f"{counter}", end="\r")
            except AttributeError:
                print("Error: ", file_)
            except KeyboardInterrupt:
                print("Manually quit.")
                break
        counter += 1
