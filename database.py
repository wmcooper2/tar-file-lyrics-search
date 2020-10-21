"""With manual edits, time to parse all song names and enter into the database took 14.23 minutes"""

from time import time

# custom
from db_util import (
        open_db,
        populate_database,
        word_list,
        words_in_dict)

tarname = "block100.tar.gz"
# tarname = "lyrics.tar.gz"
start = time()

# # TODO
# results = populate_database(tarname)

# break up song into words
songs = word_list(tarname)
# print(next(songs))


# run through each song and compare against the dictionary
dictionary = "/usr/share/dict/web2"
with open(dictionary, "r") as d:
    dict_ = d.readlines()

counter = 0
for song in songs:
    words_in_dict(song, dict_)
    counter += 1
#     print(f"{counter}", end="\r", flush=True)
    
    # quit early, for testing
    if counter >= 6:
        break




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
