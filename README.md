# Description
A CLI tool for preparing a collection of text files for later stages of a larger program (likely to be a ML program)  
Uses an SQL database to store metrics about the lyrics files.  
All 600,000+ songs are in the main, comprehensive tar.gz file.  
Smaller archive "blocks" are available for testing.  


### Operation
1. `main.py` is the main file.
    * run as `python3 main.py`
2. The general process so far is this;
    1. Populate the db using the tarfiles
        * ex: `python3 main.py --populatedb 1.tar.gz 2.tar.gz`
    2. Add the "englishScore" field and its type
        * ex: `python3 main.py --dbfield englishScore text`
    3. Calculate an english score and add it to the DB
        * ex: `python3 main.py --englishscore 1.tar.gz`


### Testing
* Can run the code on block.tar.gz
    * It has 1/16th the full song amount (~38,500)
* Can run on a larger block with 1/4th the full song amount (~154,000)


### Notes
* Having a single compressed file is way faster than dealing with the overhead of opening so many text files.
* The hope is that I can use the built in dictionary to filter out songs in foregin languages, sort songs based on how many "real" words are in the songs (may be an issue due to slang and other poetic tools)
    * I define "real" words very simply with a space delimiter.
* The only way I can see of getting a decent run time (< 1 hour) on parsing the files in the archive (for gathering metrics) would be to run concurrently on my pi-cluster. 
    * I got the estimated run time down from 273 hours to 23 hours (without using the multiprocessing module)
* I got the normalization functions to work properly, now I have to work on stemming.
* For now, I should get work on the basics of tarfile and other tools to get it ready for the cluster.


### To do
* check the problem name files in the block dirs again...
    * I though I fixed the naming issues, but they appear to have returned.


### Notes on Database Operations
* Add fields manually with;
    * `ALTER TABLE songs ADD COLUMN englishScore text;`
* Delete fields;
    * have to copy data to new table to delete a field...
* Update a single column single record value;
    * `UPDATE songs SET englishScore=99 WHERE artist="Rihanna";`
