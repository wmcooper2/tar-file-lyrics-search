"""With manual edits, time to parse all song names and enter into the database took 14.23 minutes"""

from time import time

# custom
from db_util import open_db, split_name, simple_word_count

tarname = "lyrics.tar.gz"
start = time()

# # TODO
# results = split_name(tarname)
word_count = simple_word_count(tarname)

# with open("problem_files.txt", "r") as f:
#     problems = f.read()
# text = str(['/block146/Richie Rich', 'Ratha Be Ya N', '', '', '', ''])
# print(problems.split())
# print(text in problems)
    


# # Save and close DB
# db, connection = open_db("lyrics.db")
# db.executemany('INSERT INTO songs VALUES (?,?)', results)
# connection.commit()
# connection.close()

end = time()
print(f"Time taken: {(end-start)/60} minutes")
