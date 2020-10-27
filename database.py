"""With manual edits, time to parse all song names and enter into the database took 14.23 minutes"""

from pprint import pprint
from time import time
from timeit import timeit

# custom
from db_util import (
        english_score,
        load_songs,
        normalize_words,
        open_db,
        populate_database,
        reference_dict,
        word_list)
#         words_in_dict)

tarname = "block.tar.gz"
# tarname = "lyrics.tar.gz"
start = time()
# results = populate_database(tarname)

ref_dict = reference_dict()
ref_dict = [word.lower() for word in ref_dict]
ref_dict = set(ref_dict)
songs = load_songs(tarname) # gen

# set_time = timeit(lambda: "cats" in ref_dict, number=10000)

counter = 0
for song in songs:
    normalized = normalize_words(song.split())
    score = english_score(normalized, ref_dict)
    print("score:", score)

    #for testing
    counter += 1
    if counter > 1:
        break
# TODO








# # Save and close DB
# db, connection = open_db("lyrics.db")
# db.executemany('INSERT INTO songs VALUES (?,?)', results)
# connection.commit()
# connection.close()

end = time()
time_taken = (end-start)/60
total_songs = 616500
print(f"Time taken: {time_taken} minutes")
print(f"Estimated Time (600,000+ songs): {round(((total_songs/counter)*time_taken)/60)} hours")
