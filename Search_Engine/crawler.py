"""
Author: Caroline Rinks
Implements the WebCrawler class, which collects links starting at a specified webpage,
extracts content from these links, and cleans the extracted content to be evaluated
for relevancy given a user-specified query.
"""

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import requests, re, string, sys

class WebCrawler(object):
    def __init__(self, root, verbose):
        """
        The Constructor for the WebCrawler class.

        @param self: The WebCrawler object.
        @param root: The webpage to start crawling from.
        @param verbose: Controls the verbosity of the program's output.
        @return none
        """
        self.root = root
        self.verbose = verbose
        self.depth = 1        

        self.links = []
        self.documents = []

    def get_documents(self):
        """
        Returns the list of documents created by the crawler.

        @param self: The WebCrawler object.
        @return The list of documents created by the crawler.
        """
        return self.documents

    def set_documents(self, d):
        """
        Sets the list of documents created by the crawler.

        @param self: The WebCrawler object.
        @param d: The list of documents created by the crawler.
        @return none
        """
        self.documents = d

    def get_links(self):
        """
        Returns the list of links collected by the crawler.

        @param self: The WebCrawler object.
        @return The list of links collected by the crawler.
        """
        return self.links

    def set_links(self, l):
        """
        Sets the list of links collected by the crawler.

        @param self: The WebCrawler object.
        @param l: The list of links collected by the crawler.
        @return none
        """
        self.links = l

    def collect(self, s, d):
        """
        Collects links with "utk.edu" starting at site s and “crawling” a depth of d.

        @param self: The WebCrawler object.
        @param s: The webpage to start crawling from.
        @param d: The depth the crawler should go, hard-coded to 1.
        @return none
        """
        # Define a site, header request object, and create a request.
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(s, headers=hdr)

        # Catch and print any HTTP error BeautifulSoup encounters 
        # when opening the website at the URL.
        try:
            page = urlopen(req)
        except HTTPError as err:
            print(err.code)
            if err.code == 403:
                print(err.code)
        
        # Object to parse the HTML format
        soup = BeautifulSoup(page, 'html.parser')

        link_num = 0
        link_list = []
        if self.verbose == "T":
            print("1. COLLECTING LINKS - STARTED")

        # collect all links with "utk.edu"
        # extract all anchor tags.
        for k in soup.find_all('a'):
            link = k['href']

            # prevent duplicate links.
            if not (link in link_list):
                if link[0:5] == "https":
                    link_2 = "http" + link[5:len(link)]
                elif link[0:4] == "http":
                    link_2 = "https" + link[4:len(link)]
                else:
                    continue
                if link_2 in link_list:
                    continue
            else:
                continue
                
            if "utk.edu" in link:
                link_list.append(k['href'])
                link_num += 1
                if self.verbose == "T":
                    print("COLLECTED: LINK %d" % link_num)
        
        if self.verbose == "T":
            print("1. COLLECTING LINKS - DONE")        

        self.set_links(link_list)

    def crawl(self):
        """
        Extracts and stores all relevant text from the list of collected links.

        @param self: The WebCrawler object.
        @return none
        """
        doc_list = []
        link_num = 1
        link_list = self.get_links()

        if self.verbose == "T":
            print("2. CRAWLING LINKS - STARTED")

        for i in link_list:
            doc = ""
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(i, headers=hdr)

            # Catch and print any HTTP error
            try:
                page = urlopen(req)
            except:
                continue

            soup = BeautifulSoup(page, 'html.parser')
            
            if self.verbose == "T":
                print("CRAWLING: LINK (%d/%d)" % (link_num, len(link_list)))

            # Extract text from <p> elements inside <div> elements with "entry-content" class attribute.
            div = soup.find_all('div')
            for i in div:
                entry = i.find_all(class_='entry-content')
                for j in entry:
                    p = j.find_all('p')
                    for k in p:
                        doc += k.text + ' '
        
                # Extract text from <p> elements inside <div> elements with "person_content" class attribute.
                person = i.find_all(class_='person_content')
                for c in person:
                    p = c.find_all('p')
                    for h in p:
                        doc += h.text + ' '

            # Extract text from <table> elements with "table_default" as class attribute.
            table = soup.find_all('table')
            for i in table:
                default = i.find_all(class_='table_default')
                for j in default:
                    doc += k.text + ' '

            doc_list.append(doc)
            link_num += 1

        if self.verbose == "T":
            print("2. CRAWLING LINKS - DONE")

        self.set_documents(doc_list)
            
    def clean(self):
        """
        Modifies text extracted from webpages. Returns the cleaned documents in a list.

        @param self: The WebCrawler object.
        @return The list of cleaned documents.
        """      
        docs = self.get_documents()
        documents_clean = []

        if self.verbose == "T":
            print("3. CLEANING TEXT - STARTED")

        for d in docs:
            # Remove all Unicode characters.
            d_temp = d.encode("ascii", "ignore").decode()
            # Convert all characters to lowercase.
            d_temp = d.lower()
            # Remove all Twitter handle mentions (i.e., “@UTK_EECS“ should be deleted.)
            d_temp = re.sub('@UTK.EDU', ' ', d_temp)
            # Remove all punctuation (i.e., quotes, commas, !, ?, etc.)
            d_temp = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', d_temp)
            # Remove all instances of double-spaces.
            d_temp = (" ".join(d_temp.split()))

            documents_clean.append(d_temp)

        if self.verbose == "T":
            print("3. CLEANING TEXT - DONE")

        self.set_documents(documents_clean)
        return(documents_clean)

