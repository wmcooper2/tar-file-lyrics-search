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

 
#Set up the reference dictionary
# ref_dict = word_list(dictionary)
# ref_dict = [word.lower().strip() for word in ref_dict]
# ref_dict = set(ref_dict)
ref_dict = word_set(dictionary)



#Set up the manually curated dictionary, after all songs parsed
# bad_words = word_list(manually_curated)
# bad_words = [word.lower().strip() for word in bad_words]
# bad_words = set(bad_words)
bad_words = word_set(bad_words)


#Open DB
db, connection = open_db("lyrics.db")


#Gather metrics here
songs = load_songs(tarname)  # gen of songs

#TODO
counter = 0
for song in songs:
    normalized = normalize_words(song[0].split())
    found, not_found = words_in_dict(normalized, ref_dict)  # sets
    score = english_score(len(found), len(not_found))
    score = int(score * 100)
    bad_words = not_found.union(bad_words)

    #Insert new metrics into new DB field
    #Make sure you add a field manually first
    add_score_to_db(db, score, song[1])

    #for testing
    counter += 1

    if counter >= 1:
        break

#Close DB
connection.commit()
connection.close()

save_word_list(manually_curated)


#TODO
#Read a file from the database
#give a score and save to DB

end = time()
time_taken = (end-start)/60
total_songs = 616500
print(f"Time taken: {round(time_taken, 6)} minutes")
print(f"Estimated Time (600,000+ songs): {round(((total_songs/counter)*time_taken)/60)} hours")
