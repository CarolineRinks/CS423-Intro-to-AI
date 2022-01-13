"""
Author: Caroline Rinks
Implements the SearchEngine class.
"""

from requests.models import DEFAULT_REDIRECT_LIMIT
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import numpy as np
import pandas as pd
import crawler as c
import interface as i

class SearchEngine(object):
    def __init__(self, root, mode, query, verbose, depth):
        """
        The Constructor for the SearchEngine class.

        @param self: The SearchEngine object.
        @param root: The webpage to start crawling from.
        @param mode: The mode of the user interface: Interactive (I) or Command-Line (C)
        @param query: A string supplied by the user for which to find relevant webpages.
        @param verbose: Controls the verbosity of the program's output.
        @param depth: The depth the crawler should go, hard-coded to 1.
        @return none
        """
        self.root = root
        self.mode = mode
        self.query = query
        self.verbose = verbose
        self.depth = depth

        self.tfidf_vectorizer = None
        self.df = None
            
        self.crawler = c.WebCrawler(self.root, self.verbose)
        self.interface = i.SearchInterface(self.mode, self, self.query)

        self.docs = []
        self.links = []

        self.train()

    def start(self):
        """
        Calls the SearchEngine listen() class method.

        @param self: The SearchEngine object.
        @return none
        """
        self.listen()

    def train(self):
        """
        Calls the collect(), crawl(), and clean() WebCrawler class methods
        and saves the generated links and cleaned documents to the files 
        "links.pickle" and "docs.pickle" if the files do not already exist.

        @param self: The SearchEngine object.
        @return none
        """
        try:
            dfile = open("docs.pickle", "x")
            lfile = open("links.pickle", "x")
        except:
            # load cleaned documents from "docs.pickle" if it already exists
            dfile = open("docs.pickle", "r")
            self.docs.append(dfile.read())
            dfile.close()
            self.crawler.documents = self.docs

            # load crawled links from "links.pickle" if it already exists
            with open("links.pickle", "r") as lfile:
                line = lfile.readline()
                while line:
                    self.links.append(line)
                    line = lfile.readline()
            lfile.close()
            self.crawler.links = self.links

            self.df = self.compute_tf_idf()
            return

        # Generate crawled links and cleaned documents
        self.crawler.collect(self.root, self.depth)
        self.crawler.crawl()
        self.docs = self.crawler.clean()

        # Save cleaned documents to "docs.pickle"
        for doc in self.docs:
            dfile.write(doc)
            dfile.write("\n\n")
        dfile.close()

        # Save links to "links.pickle"
        self.links = self.crawler.get_links()
        for link in self.links:
            lfile.write(link)
            lfile.write("\n")
        lfile.close()

        self.df = self.compute_tf_idf()
        return

    def delete(self):
        """
        Deletes any .pickle files created from the SearchEngine class's train() method.

        @param self: The SearchEngine object.
        @return none
        """
        os.remove("docs.pickle")
        os.remove("links.pickle")

    def compute_tf_idf(self):
        """
        Reads and Vectorizes all cleaned documents using Scikit-Learn's TfidfVectorizor.

        @param self: The SearchEngine object.
        @return none
        """
        # Instantiate the Tfidfvectorizer
        self.tfidf_vectorizer = TfidfVectorizer()

        # Send docs into the Vectorizer
        tfidf_vectorizer_vectors = self.tfidf_vectorizer.fit_transform(self.docs)

        # Transpose the result into a more traditional TF-IDF matrix and convert it to an array.
        X = tfidf_vectorizer_vectors.T.toarray()

        # Convert the matrix into a dataframe using feature names as the dataframe index.
        df = pd.DataFrame(X, index=self.tfidf_vectorizer.vocabulary)
        return df

    def handle_query(self, query):
        """
        Evaluates the relevance of webpages by calculating the cosine similarity
        between the query and each extracted document. Up to the 5 most relevant
        webpages are outputted to the user. 

        @param self: The SearchEngine object.
        @param query: The string supplied by the user for which to find relevant webpages for.
        @return none
        """
        # Vectorize the query.
        q = [query]
        q_vec = self.tfidf_vectorizer.transform(q).toarray().reshape(self.df.shape[0],)

        # Calculate cosine similarity between query and all documents. 
        sim = {}
        for i in range(len(self.df.columns)):
            sim[i] = np.dot(self.df.loc[:, i].values, q_vec) / np.linalg.norm(self.df.loc[:, i]) * np.linalg.norm(q_vec)

        # Sort results.
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)

        # Print a list of up to 5 documents that are relevant to the query.
        printed = 0
        for k, v in sim_sorted:
            if printed == 5:
                return
            if v != 0.0 and not(np.isnan(v)):
                printed += 1
                print("[%d] %s (%.2f)" % (printed, (self.crawler.get_links())[k].rstrip(), v))
        if printed == 0:
            print("Your search did not match any documents. Try again.")

    def listen(self):
        """
        Calls the SearchInterface listen() class method.

        @param self: The SearchEngine object.
        @return none
        """
        self.interface.listen()
