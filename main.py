# std lib
import argparse
import re
import tarfile
from typing import Generator, TypeVar

# custom
from db_util import create_db, get_file_info, search


match = TypeVar("match", re.match, None)
tarData = TypeVar("tar", tarfile.TarFile, None)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
#     parser.add_argument('--dbsetup', action='store_true', help="Setup a new database")

    setup = parser.add_mutually_exclusive_group()
    setup.add_argument('--dbpartial', action='store_true', help="Setup a new database")
    setup.add_argument('--dbpopulate', action='store_true', help="Setup a new database")
    setup.add_argument('--search', action='store_true', help="Setup a new database")
    setup.add_argument('--estimatetime', action='store_true', help="Setup a new database")

    args = parser.parse_args()

    if args.dbpartial:
        #Create DB
        db, connection = create_db("lyrics.db")
#         tarname = "2.tar.gz"
        tarname = "block.tar.gz"
        file_info = get_file_info(tarname)

        #Add file_info to DB
        db.executemany('INSERT INTO songs VALUES (?,?,?)', file_info)
        connection.commit()
        connection.close()

    if args.dbpopulate:
        #Create DB
        db, connection = create_db("lyrics.db")
        
        for x in range(1, 5):  # all the files 
            tarname = f"{str(x)}.tar.gz"
            file_info = get_file_info(tarname)

        #Add file_info to DB
        db.executemany('INSERT INTO songs VALUES (?,?,?)', file_info)
        connection.commit()
        connection.close()

    if args.search:
        print("searching")
#         search("what is", name)

    if args.estimatetime:
        print("estimating time to complete")

        
