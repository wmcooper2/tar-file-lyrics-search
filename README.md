# Searching through archived lyrics files
Use an SQL database to store metrics about the lyrics files.  
All 600,000+ songs are in a single tar.gz file.  

### Operation
Not intended to be run as a standalone program for anything but to help me clean up the data in order to feed into machine learning projects.
1. `database.py` is the main file.
    * comment out the lines that you don't need to avoid adding records to the database
    * run as `python3 database.py`



### Notes
* Working on how I want to classify words as "bad/good" by using the built-in dict "/usr/shar/dict/web2" (macOS)
* The hope is that I can use the built in dictionary to filter out songs in foregin languages, sort songs based on how many "real" words are in the songs (may be an issue due to slang and other poetic tools)
* The only way I can see of getting a decent run time on parsing the files in the archive (for gathering metrics) would be to run concurrently on my pi-cluster. 
    * Currently, I estimated that a run through of simply checking if each word from each song is in the built-in dictionary would take 273 hours on my macbook.
    * I can get this down to about 17 hours (rough guess, without optimizations) by using multiprocessing using all 16 cores of my pi-cluster.
    
* For now, I should get work on the basics of tarfile and other tools to get it ready for the cluster.
