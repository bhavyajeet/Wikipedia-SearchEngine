The code for final index creation is split into 3 files. 
1) indexer.py
2) merger.py
3) splitter.py
indexer.py creates the entire index in parts. every index file created by index.py contains the index obtained from a certain threshhold of documents.
merger.py merges these parted index files into one common huge index file.
splitter.py splits the huge index file generated by merger.py into small peices to make the search query faster.
The fintitle folder contains various files which contain the title of the documents which are parsed to create the index to return as outputs of the search query. 
Each file contains a certain threshhold (1500) of title names to make the query faster. 
