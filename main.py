# std lib
import argparse
from typing import Generator

# custom
from db_util import create_db, add_column
from file_util import get_file_info, search
from gather_metrics import add_english_score_to_db


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Preprocess data files to be used in a larger ML program.')
    setup = parser.add_mutually_exclusive_group()
    setup.add_argument('--populatedb', action='store', nargs="+", metavar=("TARFILE"), help="Populate the DB with all the songs.")
    setup.add_argument('--search', action='store', nargs=2, type=str, metavar=("PATTERN", "TARFILE"), help="Search for PATTERN in TARFILE.")
    setup.add_argument('--estimatetime', action='store_true', help="Estimate the time required to run the code on the entire collection of songs.")
    setup.add_argument('--test', action='store_true', help="Run tests.")
    setup.add_argument('--dbfield', action='store', nargs=2, type=str, metavar=("NAME", "TYPE"), help="Add a column to the DB with label NAME and type TYPE.")
    setup.add_argument('--englishscore', action='store', nargs=1, metavar=("TARFILE"), help="Calculate score for how many English words were found, then add to the DB.")

    args = parser.parse_args()

    if args.populatedb:
        db, connection = create_db("lyrics.db")
        for tarname in args.populatedb:
            file_info = get_file_info(tarname)
            db.executemany('INSERT INTO songs VALUES (?,?,?)', file_info)

        #Add file_info to DB
        connection.commit()
        connection.close()

    if args.search:
        print(f"searching for {args.search[0]}, {args.search[1]}")
        search(args.search[0], args.search[1])

    if args.estimatetime:
        print("estimating time to complete")

    if args.dbfield:
        add_column(args.dbfield[0], args.dbfield[1])
        print(f"Added {args.dbfield[0]} column as type {args.dbfield[1]}")

    if args.englishscore:
#         print(args.englishscore)
        add_english_score_to_db(args.englishscore[0])
