# Searching through archived lyrics files
Use an SQL database to store metrics about the lyrics files.  
All 600,000+ songs are in a single tar.gz file.  

### Operation
Not intended to be run as a standalone program for anything but to help me clean up the data in order to feed into machine learning projects.
1. `database.py` is the main file.
    * comment out the lines that you don't need to avoid adding records to the database
    * run as `python3 database.py`


### Testing
1. Run the code on block.tar.gz
    * It has 1/16th the full song amount (~616,000 / 16)


### Notes
* Having a single compressed file is way faster than dealing with the overhead of opening so many text files.
* The hope is that I can use the built in dictionary to filter out songs in foregin languages, sort songs based on how many "real" words are in the songs (may be an issue due to slang and other poetic tools)
* The only way I can see of getting a decent run time (< 1 hour) on parsing the files in the archive (for gathering metrics) would be to run concurrently on my pi-cluster. 
    * I got the estimated run time down from 273 hours to 23 hours (without using the multiprocessing module)
* I got the normalization functions to work properly, now I have to work on stemming.
* For now, I should get work on the basics of tarfile and other tools to get it ready for the cluster.
