# std lib
import argparse
from collections import namedtuple, defaultdict
import csv
from datetime import datetime
from pprint import pprint
import re
import tarfile
from typing import Any, Generator, List, TypeVar


# 3rd party
from tabulate import tabulate


# custom
from constants import (
    ENG_TARBALL,
    RESULTS,
    SEARCH_DESC,
    UNCOMPRESSED_TESTING,
    VOCAB_TARBALL)
from metrics_util import edit_distance
from file_util import remove_all_digits, remove_all_punct


tarData = TypeVar("tar", tarfile.TarFile, None)
match = TypeVar("match", re.match, None)
Song = namedtuple("Song", ["artist", "name"])

#TODO
# check if a search was already performed by looking for the search string in the title of the results file then ask the user if they want to proceed.
# are the --song and --lyrics options the same thing?


if __name__ == "__main__":

    #Load description
    with open(SEARCH_DESC) as f:
        how_to_use = f.read()

    parser = argparse.ArgumentParser(prog="Search" ,formatter_class=argparse.RawDescriptionHelpFormatter, description=how_to_use)
    parser.add_argument("--artist", action="store", nargs=1, type=str, metavar=("ARTIST"), help="Search for a specfic ARTIST.")
    parser.add_argument("--lyrics", action="store", nargs=1, type=str, metavar=("SONG"), help="Search for a specfic SONG's lyrics and print to terminal.")
    parser.add_argument("--song", action="store", nargs=1, type=str, metavar=("SONG"), help="Search for a specfic SONG.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--regex", action="store", nargs=2, type=str, metavar=("REGEX", "STRING"), help="Search for a grammar pattern using the given REGEX and save to results/STRING.")
    group.add_argument("--sentence", action="store", nargs=1, type=str, metavar=("STRING"), help="Search for a specfic STRING.")
    group.add_argument("--sentencelist", action="store", nargs="?", type=argparse.FileType("r"), metavar=("FILE"), help="Search for a list of specfic strings.")
    group.add_argument("--vocablist", action="store", nargs="?", type=argparse.FileType("r"), metavar=("FILE"), help="Search for a list of vocab words from FILE")

    args = parser.parse_args()

#ARTIST
    if args.artist:
        original_request = args.artist[0]

        #Open tarball
        songs = tarfile.open(ENG_TARBALL)
#         songs = tarfile.open(UNCOMPRESSED_TESTING)

        #Get memberlist
        print("Collecting archives...")
        archives = songs.getmembers()
        total_archives = len(archives)

        #Normalize user request
        print(f"Searching for '{original_request}'")
        user_request = remove_all_digits(original_request)
        user_request = remove_all_punct(user_request)
        user_request = user_request.lower()

        results = defaultdict(int)
        for archive in enumerate(archives):
            #Clean up title
            artist, song = archive[1].name.rstrip(".txt").split("_")

            #normalize the strings for comparison
            artist = remove_all_digits(artist)
            artist = remove_all_punct(artist)
            artist = artist.lower()
            edit_score = edit_distance(user_request, artist)

            #songs may share the same name, keep all
            results[archive[1].name] = edit_score
            print(f"{archive[0]}/{total_archives}", end="\r", flush=True)
    
        #sort list of matches by value
        results = list(results.items())
        top_100 = sorted(results, key=lambda x: x[1])
        top_100 = top_100[:100]

        #Save to results/
        timestamp = "{:%Y-%b-%d %H:%M:%S}".format(datetime.now())
        with open(f"{RESULTS}{original_request}_{timestamp}.txt", "w+") as save_to:
            save_to.write(tabulate(top_100))

        print("\nA smaller Edit Distance means a closer match.")
        print(tabulate(top_100[:10], headers=["Artist_Song", "Edit Distance"]))
        songs.close()
        quit()

    elif args.lyrics:
        print("searching for lyrics")
        original_request = args.lyrics[0]

        #Open tarball
        songs = tarfile.open(ENG_TARBALL)
#         songs = tarfile.open(UNCOMPRESSED_TESTING)

        #Get memberlist
        print("Collecting archives...")
        archives = songs.getmembers()
        total_archives = len(archives)

        #Normalize user request
        print(f"Searching for '{original_request}'")
        user_request = remove_all_digits(original_request)
        user_request = remove_all_punct(user_request)
        user_request = user_request.lower()

        results = []
        for archive in enumerate(archives):
            #Clean up title
            artist, song = archive[1].name.rstrip(".txt").split("_")

            #normalize the strings for comparison
            song = remove_all_digits(song)
            song = remove_all_punct(song)
            song = song.lower()
            edit_score = edit_distance(user_request, song)

            #songs may share the same name, keep all
            artist, song = archive[1].name.rstrip(".txt").split("_")
            results.append((artist, song, edit_score))
            print(f"{archive[0]}/{total_archives}", end="\r", flush=True)

        top_100 = sorted(results, key=lambda x: x[2])
        last_100 = top_100[-100:]
        top_100 = top_100[:100]

        #Show results, have user pick one to show
        print("\nA smaller Edit Distance means a closer match.")
        top_10 = [[x[0], x[1][0], x[1][1], x[1][2]] for x in enumerate(top_100[:10])]
        print(tabulate((top_10), headers=["Index", "Artist", "Song", "Edit Distance"]))

        #Extract to memory and print to the screen
        while True:
            view_extract = input("View [v], extract [e] to dir or quit [q]? ")
            if view_extract == "v":
                answer = int(input("Which one do you want to view? [index #] "))
                artist = top_10[answer][1]
                song = top_10[answer][2]
                title = f"{artist}_{song}.txt"
                text = songs.extractfile(title).read().decode("utf-8")
                header = f"\n{artist}, {song}"
                print(header)
                print("-"*len(header))
                print(text)
            elif view_extract == "e":
                #TODO, Give user option to save file to a dir
                dir_ = input("extract to where? ")
                print(f"Extracting to {dir_}")
                break
            elif view_extract == "q":
                break
            else:
                print("Choose one of [veq].")
        songs.close()
        quit()


#SONG
    elif args.song:
        original_request = args.song[0]

        #Open tarball
        songs = tarfile.open(ENG_TARBALL)
#         songs = tarfile.open(UNCOMPRESSED_TESTING)

        #Get memberlist
        print("Collecting archives...")
        archives = songs.getmembers()
        total_archives = len(archives)

        #Normalize user request
        print(f"Searching for '{original_request}'")
        user_request = remove_all_digits(original_request)
        user_request = remove_all_punct(user_request)
        user_request = user_request.lower()

        results = defaultdict(int)
        for archive in enumerate(archives):
            #Clean up title
            artist, song = archive[1].name.rstrip(".txt").split("_")

            #normalize the strings for comparison
            song = remove_all_digits(song)
            song = remove_all_punct(song)
            song = song.lower()
            edit_score = edit_distance(user_request, song)

            #songs may share the same name, keep all
            results[archive[1].name] = edit_score
            print(f"{archive[0]}/{total_archives}", end="\r", flush=True)

        #sort list of matches by value
        results = list(results.items())
        top_100 = sorted(results, key=lambda x: x[1])
        top_100 = top_100[:100]

        #Save to results/
        timestamp = "{:%Y-%b-%d %H:%M:%S}".format(datetime.now())
        with open(f"{RESULTS}{original_request}_{timestamp}.txt", "w+") as save_to:
            save_to.write(tabulate(top_100))

        print("\nA smaller Edit Distance means a closer match.")
        print(tabulate(top_100[:10], headers=["Artist_Song", "Edit Distance"]))
        songs.close()
        quit()


#REGEX
    elif args.regex:
        """Basically, this block is supposed to be the same as a regular sentence search,
            but uses a regex in its place."""
        regex = args.regex[0]
        save_name = args.regex[1]
        pattern = re.compile(regex, re.IGNORECASE)
        songs = tarfile.open(ENG_TARBALL)

        #get memberlist
        print("Collecting archives...")
        archives = songs.getmembers()
        total_archives = len(archives)

        print(f"Searching for '{regex}'")
        results = defaultdict(int)
        for archive in enumerate(archives):
            #extract archive to memory
            lyrics = songs.extractfile(archive[1])

            #perform regex search on archive
            lyrics = lyrics.read().decode("utf-8")
            match_count = len(pattern.findall(lyrics))

            #save count of all occurrences in list, use bisect to insert based on count
            print(f"{archive[0]}/{total_archives}", end="\r", flush=True)

            # if any matches
            if match_count > 0:
                name = archive[1].name.rstrip(".txt")
                results[name] += match_count
    
        #sort list of matches by value
        results = list(results.items())
        top_100 = sorted(results, key=lambda x: x[1], reverse=True)
        top_100 = top_100[:100]

        #Save to results/
        timestamp = "{:%Y-%b-%d %H:%M:%S}".format(datetime.now())
        with open(f"{RESULTS}{save_name}_{timestamp}.csv", "w+") as save_to:
            writer = csv.writer(save_to, delimiter="|")
            for result in top_100:
                artist, song = result[0].split("_")
                match_count = result[1]
                row = [artist, song, str(match_count)]
                try:
                    writer.writerow(row)
                except:
                    continue

        songs.close()
        print(f"\nSearch for '{regex}' finished.")



#SENTENCE, or SINGLE VOCABULARY WORD
    elif args.sentence:
        search_string = args.sentence[0]
        songs = tarfile.open(ENG_TARBALL)
        pattern = re.compile(args.sentence[0], re.IGNORECASE)

        #get memberlist
        print("Collecting archives...")
        archives = songs.getmembers()
        total_archives = len(archives)

        print(f"Searching for '{search_string}'")
        results = defaultdict(int)
        for archive in enumerate(archives):
            #extract archive to memory
            lyrics = songs.extractfile(archive[1])

            #perform regex search on archive
            lyrics = lyrics.read().decode("utf-8")
            match_count = len(pattern.findall(lyrics))

            #save count of all occurrences in list, use bisect to insert based on count
            print(f"{archive[0]}/{total_archives}", end="\r", flush=True)

            # if any matches
            if match_count > 0:
                name = archive[1].name.rstrip(".txt")
                results[name] += match_count
    
        #sort list of matches by value
        results = list(results.items())
        top_100 = sorted(results, key=lambda x: x[1], reverse=True)
        top_100 = top_100[:100]

        #Save to results/
        timestamp = "{:%Y-%b-%d %H:%M:%S}".format(datetime.now())
        with open(f"{RESULTS}{search_string}_{timestamp}.csv", "w+") as save_to:
            writer = csv.writer(save_to, delimiter="|")
            for result in top_100:
                artist, song = result[0].split("_")
                match_count = result[1]
                row = [artist, song, str(match_count)]
                try:
                    writer.writerow(row)
                except:
                    continue

        songs.close()
        print(f"\nSearch for '{search_string}' finished.")

        #TODO, make note of using quit... 
        #   try using break instead so that I get to see the other print statments
        #TODO, the lyrics themselves are not normalized, 
        #   so there may be many false negative matches
        #   using case-insensitive matching helps, but there's the issue of the punctuation


    elif args.sentencelist:
        """Basically, this block is supposed to be the same as a regular sentence sentence search,
            but placed within a for loop."""

        sentences = args.sentencelist.readlines()
        print("sentences:", sentences)

        #get memberlist
        print("Collecting archives...")
        songs = tarfile.open(ENG_TARBALL)
        archives = songs.getmembers()
        total_archives = len(archives)

        #forloop this
        for sentence in sentences:
            sentence = sentence.strip()
            pattern = re.compile(sentence, re.IGNORECASE)

            print(f"Searching for '{sentence}'")
            results = defaultdict(int)
            for archive in enumerate(archives):
                #extract archive to memory
                lyrics = songs.extractfile(archive[1])

                #perform regex search on archive
                lyrics = lyrics.read().decode("utf-8")
                match_count = len(pattern.findall(lyrics))

                #save count of all occurrences in list, use bisect to insert based on count
                print(f"{archive[0]}/{total_archives}", end="\r", flush=True)

                # if any matches
                if match_count > 0:
                    name = archive[1].name.rstrip(".txt")
                    results[name] += match_count
        
            #sort list of matches by value
            results = list(results.items())
            top_100 = sorted(results, key=lambda x: x[1], reverse=True)
            top_100 = top_100[:100]

            #Save to results/
            timestamp = "{:%Y-%b-%d %H:%M:%S}".format(datetime.now())
            with open(f"{RESULTS}{sentence}_{timestamp}.csv", "w+") as save_to:
                writer = csv.writer(save_to, delimiter="|")
                for result in top_100:
                    artist, song = result[0].split("_")
                    match_count = result[1]
                    row = [artist, song, str(match_count)]
                    try:
                        writer.writerow(row)
                    except:
                        continue
            print(f"\nSearch for '{sentence}' finished.", end="\n", flush=True)
        songs.close()



#VOCABULARY LIST
    #TODO, the scoring/ranking is off, can't have a score of 1500 but yet it does...
    elif args.vocablist:
        #Load files
        words = args.vocablist.read()
        songs = tarfile.open(VOCAB_TARBALL)

        #get memberlist
        print("Collecting archives...")
        archives = songs.getmembers()
        total_archives = len(archives)

        print(f"Searching for vocabulary...")
        results = defaultdict(int)
        for archive in enumerate(archives):
            lyrics = songs.extractfile(archive[1])
            lyrics = lyrics.read().decode("utf-8")
            
            #search for each word, calculate match ratio
            match_count = 0
            for word in words:
                if word.strip() in lyrics:
                    match_count += 1
            match_ratio = int((match_count/len(lyrics)) * 100)

            #save in dictionary
            name = archive[1].name.rstrip(".txt")
            results[name] += match_ratio
            print(f"{archive[0]}/{total_archives}", end="\r", flush=True)

        #sort list of matches by value
        results = list(results.items())
        top_100 = sorted(results, key=lambda x: x[1], reverse=True)
        top_100 = top_100[:100]

        #Save to results/
        timestamp = "{:%Y-%b-%d %H:%M:%S}".format(datetime.now())
        save_to = f"{RESULTS}vocabulary_{timestamp}.csv"
        with open(save_to, "w+") as save_to:
            writer = csv.writer(save_to, delimiter="|")
            for result in top_100:
                artist, song = result[0].split("_")
                match_ratio = result[1]
                row = [artist, song, str(match_ratio)]
                try:
                    writer.writerow(row)
                except:
                    continue

        songs.close()
        print(f"\nFinished searching. Look in {save_to} for your results.")
