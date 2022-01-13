"""
Author: Caroline Rinks
Instantiates a SearchEngine object. Implements a simple search engine that
takes a user-supplied query and finds relevant webpages by calculating the 
cosine-similarity between the query and each webpage.
"""
import engine as e
import sys

def parse_args():
    """
    Parses command-line arguments root, mode, query, and verbose.

    @return root: The webpage to start crawling from.
    @return mode: The mode of the user interface: Interactive (I) or Command-Line (C)
    @return query: A string supplied by the user for which to find relevant webpages.
    @return verbose: Controls the verbosity of the program's output.
    """
    root = ""
    mode = ""
    query = ""
    verbose = ""
    
    # Parse arguments and check validity
    for i in range(0, len(sys.argv)):
        if (sys.argv[i] == "-root"):
            if (i+1 == len(sys.argv)):
                sys.exit("ERROR: Missing required arguments")

            root = sys.argv[i+1]
            if not(root[0:4] == "http" or root[0:5] == "https"):
                sys.exit("ERROR: Invalid arguments provided")
        elif (sys.argv[i] == "-mode"):
            if (i+1 == len(sys.argv)):
                sys.exit("ERROR: Missing required arguments")

            mode = sys.argv[i+1]
            if not(mode == "C" or mode == "I"):
                sys.exit("ERROR: Invalid arguments provided")
        elif (sys.argv[i] == "-query"):
            if (i+1 == len(sys.argv)):
                break

            query = sys.argv[i+1]
        elif (sys.argv[i] == "-verbose"):
            if (i+1 == len(sys.argv)):
                break

            verbose = sys.argv[i+1]
            if not(verbose == "T" or verbose == "F"):
                sys.exit("ERROR: Invalid arguments provided")

    if root == "" or mode == "":
        sys.exit("ERROR: Missing required arguments")
    elif mode == "C":
        if query == "":
            sys.exit("ERROR: Missing query argument")
    elif mode == "I":
        if verbose == "":
            sys.exit("ERROR: Missing verbose argument")

    return root, mode, query, verbose

def main():
    args = parse_args()
    root = args[0]
    mode = args[1]
    query = args[2]
    verbose = args[3]

    engine = e.SearchEngine(root, mode, query, verbose, depth=1)
    engine.start()

if __name__ == '__main__':
    main()

