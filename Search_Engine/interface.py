"""
Author: Caroline Rinks
Implements the SearchInterface class, which implements one of two 
simple interfaces: an interactive search query or a command-line interface.
"""

class SearchInterface(object):
    def __init__(self, mode, engine, query):
        """
        The Constructor for the SearchInterface class.

        @param self: The SearchInterface object.
        @param mode: The mode of the user interface: Interactive (I) or Command-Line (C)
        @param engine: A SearchEngine object that holds the SearchInterface instance.
        @param query: A string supplied by the user for which to find relevant webpages.
        @return none
        """
        self.mode = mode
        self.engine = engine
        self.query = query

    def listen(self):
        """
        Implements a command line loop if the UI mode is interactive.
        Otherwise, it handles a single query supplied by the user.

        @param self: The SearchInterface object.
        @return none
        """
        if self.mode == "C":
            # Command Line Mode - Send Query to Search Engine
            self.engine.handle_query(self.query)
        else:
            # Interactive Mode
            print("-----------------------------------")
            print("|         UTK EECS Search         |")
            print("-----------------------------------")

            while True:
                command = input("> ")
                if command == ":exit":
                    break
                self.query = command
                self.handle_input()
                 
    def handle_input(self):
        """
        Routes queries and commands when using the Interactive UI mode. 
        Valid commands are :delete and :train. Anything else is considered a query.

        @param self: The SearchInterface object.
        @return none
        """
        if self.query == ":train":
            self.engine.train()
        elif self.query == ":delete":
            self.engine.delete()
        else:
            self.engine.handle_query(self.query)
