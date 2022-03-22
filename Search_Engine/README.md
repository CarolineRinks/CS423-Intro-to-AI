Author: Caroline Rinks

**UTK Search Engine**

-----------
Description
-----------
This program implements a basic search engine for .utk websites with an embedded web crawler 
alongside a ranking and retrieval system. This is accomplished with 3 classes: a WebCrawler 
class that scrapes and stores data from UTK-affiliated websites, a SearchInterface class 
that creates either an interactive or command-line interface for issuing search queries, and 
a SearchEngine class which instantiates the WebCrawler and SearchInterface classes while also 
storing and calculating webpage relevance using TF-IDF indexing and cosine similarity scoring.

-----
Usage
-----
To run this program, navigate to the directory where main.py is stored and type 
the following command into a terminal: 
	
	python main.py -root ROOT -mode C|I [-query QUERY] [-verbose T|F]

Example of a valid command:
	
	python main.py -root https://eecs.utk.edu -mode C -query lab -verbose T

-------------
.pickle files
-------------
The generated file docs.pickle contains the scraped text from each webpage and links.pickle contains the
links found on each webpage. The docs.pickle and links.pickle files in this folder were generated 
with the following command:

	python main.py -root https://eecs.utk.edu -mode C -query undergraduate -verbose F
