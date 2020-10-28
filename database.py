from time import time
from timeit import timeit

# custom
from db_util import (
        english_score,
        lazy_word_list,
        load_songs,
        normalize_words,
        open_db,
        populate_database,
        word_list)


#Populate the database with the basics
for x in range(1, 5):
    tarname = f"{str(x)}.tar.gz"
    results = populate_database(tarname)

#Save and close DB
db, connection = open_db("lyrics.db")
db.executemany('INSERT INTO songs VALUES (?,?)', results)
connection.commit()
connection.close()

#Testing DB population
# tarname = "1.tar.gz"
# results = populate_database(tarname)


start = time()
# tarname = "block.tar.gz"
manually_curated = "manually_curated_words.txt"
dictionary = "/usr/share/dict/web2"
 
#set up the reference dictionary
ref_dict = word_list(dictionary)
ref_dict = [word.lower().strip() for word in ref_dict]
ref_dict = set(ref_dict)
songs = load_songs(tarname) # gen

#set up the manually curated dictionary, after all songs parsed
# recoverable_words = word_list(manually_curated)
# print("rec", recoverable_words[:10])
# recoverable_words = set(recoverable_words)

#normalize lyrics and give score
# counter = 0
# for song in songs:
#     normalized = normalize_words(song.split())
#     score = english_score(normalized, ref_dict)
#     print("score:", score)
# 
#     #for testing
#     counter += 1
#     if counter > 1:
#         break

# # TODO
#Add field to DB for score
#Read a file from the database
#give a score and save to DB


end = time()
time_taken = (end-start)/60
total_songs = 616500
# print(f"Time taken: {round(time_taken, 6)} minutes")
# print(f"Estimated Time (600,000+ songs): {round(((total_songs/counter)*time_taken)/60)} hours")
