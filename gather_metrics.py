# std lib
from pprint import pprint
from time import time
from timeit import timeit


# custom
from db_util import (
    add_score_to_db,
    open_db)
from metrics_util import (
    english_score,
    load_songs,
    normalize_words,
    save_word_list,
    words_in_dict,
    word_set)


# make the timing setup a decorator
start = time()
tarname = "2.tar.gz"
manually_curated = "manually_curated_words.txt"
dictionary = "/usr/share/dict/web2"

# setup for gathering metrics
ref_dict = word_set(dictionary)
bad_words = word_set(manually_curated)
db, connection = open_db("lyrics.db")
songs = load_songs(tarname)  # gen of songs



#TODO
# This whole block's purpose is to calculate a ratio of good English words
counter = 0
for song in songs:
    score = english_score(song, ref_dict)
#     bad_words = not_found.union(bad_words)
#     add_score_to_db(db, score, song[1])

# testing
    counter += 1
    if counter >= 5:
        break

#Close DB
connection.commit()
connection.close()

# save_word_list(manually_curated, bad_words)


#TODO
#Read a file from the database
#give a score and save to DB

end = time()
time_taken = (end-start)/60
total_songs = 616500
print(f"Time taken: {round(time_taken, 6)} minutes")
print(f"Estimated Time (600,000+ songs): {round(((total_songs/counter)*time_taken)/60)} hours")
