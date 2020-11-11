# std lib
import argparse
from typing import Generator

# custom
from db_util import create_db, add_column
from file_util import get_file_info, search



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Preprocess data files to be used in a larger ML program.')
    setup = parser.add_mutually_exclusive_group()
    setup.add_argument('--dbpartial', action='store_true', help="Setup a new database with a subset of the total songs.")
    setup.add_argument('--dbpopulate', action='store_true', help="Populate the DB with all the songs.")
    setup.add_argument('--search', action='store', nargs=2, type=str, metavar=("PATTERN", "TARFILE"), help="Search for PATTERN in TARFILE.")
    setup.add_argument('--estimatetime', action='store_true', help="Estimate the time required to run the code on the entire collection of songs.")
    setup.add_argument('--test', action='store_true', help="Run tests.")
    setup.add_argument('--dbfield', action='store', nargs=2, type=str, metavar=("NAME", "TYPE"), help="Add a column to the DB with label NAME and type TYPE.")

    args = parser.parse_args()

    if args.dbpartial:
        db, connection = create_db("lyrics.db")
#         tarname = "2.tar.gz"
        tarname = "block.tar.gz"
        file_info = get_file_info(tarname)

        #Add file_info to DB
        db.executemany('INSERT INTO songs VALUES (?,?,?)', file_info)
        connection.commit()
        connection.close()

    if args.dbpopulate:
        db, connection = create_db("lyrics.db")
        for x in range(1, 5):  # all the files 
            tarname = f"{str(x)}.tar.gz"
            file_info = get_file_info(tarname)

        #Add file_info to DB
        db.executemany('INSERT INTO songs VALUES (?,?,?)', file_info)
        connection.commit()
        connection.close()

    if args.search:
        print(f"searching for '{args.search[0]}'")
        print(f"searching for '{args.search[1]}'")
        search(args.search[0], args.search[1])

    if args.estimatetime:
        print("estimating time to complete")

    if args.dbfield:
        print(args.dbfield)
        add_column(args.dbfield[0], args.dbfield[1])
