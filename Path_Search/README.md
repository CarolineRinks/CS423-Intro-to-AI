Author: Caroline Rinks
Name: Project 2 (Search)

------------
Instructions
------------
    To run this program, navigate to the directory where main.py is stored and type 
    the following command into a terminal:
        python3 main.py --input FILENAME --start START_NODE --goal GOAL_NODE --search SEARCH_TYPE
    
    FILENAME, START_NODE, GOAL_NODE, and SEARCH_TYPE are all specified by the user.

-----------
Description
-----------
    This program contains a PathPlanner class which defines three search
    methods: DFS, BFS, and A*. The program processes a file containing 
    the specifications for a grid environment. A search is then carried out 
    according to the type specified by the user. The program will output the 
    shortest path from the specified start coordinate to the goal coordinate if 
    one is found, as well as the total number of nodes traversed during the search.

