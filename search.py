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


def extract_file_contents(file_name: str, name: tarData) -> bytes:
    """Get the archived file's contents."""
    with tarfile.open(name) as tar:
        data = tar.extractfile(file_name)
        return data.read().decode("utf-8")


def search(pattern: str, name: str) -> match:
    matches = 0
    counter = 0
    with tarfile.open(name=name, mode="r") as tar:
        for file_ in tar:
            t = tar.getmember(file_.name)
            if t.isfile():
                try:
                    contents = extract_file_contents(t, name)
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
            counter += 1



# name = "lyrics.tar.gz"
name = "block100.tar.gz"
search("what is", name)
