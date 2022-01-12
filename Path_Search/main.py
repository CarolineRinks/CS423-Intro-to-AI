'''
Author: Caroline Rinks
This program reads in a file containing a grid environment and finds the shortest path
between a specified start and end coordinate location.
'''

import sys

class Node(object):
    def __init__(self, x, y, parent=None):
        """
        The Constructor for the Node Class.
        
        @param self: The Node object
        @param x: A node's x-coordinate
        @param y: A node's y-coordinate
        @param parent: A node's parent, defaults to None if not specified
        @return none
        """
        
        self.x = int(x)
        self.y = int(y)
        self.parent = parent
        self.children = []
        self.height = 0
        self.h_val = 1000
        self.g_val = 1000

        if not parent is None:
            parent.addChild(self)

    def addChild(self, child):
        """
        Given a child, adds the child to the Node object's list of children.

        @param self: The Node object
        @param child: The node being added to self's list of children
        @return none
        """
        child.setHeight(self)
        self.children.append(child)

    def setHeight(self, parent):
        """
        Sets a Node's height, which is 1 more than its parent's.

        @param self: The Node object
        @param parent: The Node's parent
        @return none
        """
        self.height = parent.height + 1

    def getH_val(self):
        """
        Returns a Node's h(x) value.

        @param self: The Node object
        @return A node's h(x) value
        """
        return self.h_val

    def getG_val(self):
        """
        Returns a Node's g(x) value.

        @param self: The Node object
        @return A node's g(x) value
        """
        return self.g_val

    def getX(self):
        """
        Returns a Node's x-coordinate.

        @param self: The Node object
        @return A node's x-coordinate
        """
        return self.x
    
    def getY(self):
        """
        Returns a Node's y-coordinate.

        @param self: The Node object
        @return A node's y-coordinate
        """
        return self.y

class PathPlanner(object):
    def __init__(self, Nrows, Ncols):
        """
        The Constructor for the class PathPlanner.
        
        @param self: The PathPlanner object
        @param Nrows: The number of rows in the grid environment
        @param Ncols: The number of columns in the grid environment
        @return none
        """
        
        self.Nrows = Nrows
        self.Ncols = Ncols
        self.count = 0

        self.stack = []
        self.queue = []
        self.visited_str = []

    def calculate_hx(self, node, goal):
        """
        Given a current node and a goal node, calculate and set the current node's h(x) value,
        which is the Euclidean distance from the current node to the goal node.
        
        @param self: The PathPlanner object
        @param node: The current node to calculate h(x)
        @param goal: The goal node
        @return none
        """

        if node.getX() == goal.getX() and node.getY() == goal.getY() :
            node.h_val = 0
            return

        x2 = goal.getX()
        y2 = goal.getY()
        x1 = node.getX()
        y1 = node.getY()
                
        Euclidean_dis =  ( ((x2-x1)**2) + ((y2-y1)**2) )**0.5
        node.h_val = Euclidean_dis

    def calculate_gx(self, node, child):
        """
        Given a current node and its child, calculate and set the child node's g(x) value,
        which is equivalent to the number of movements taken from the starting position.
        
        @param self: The PathPlanner object
        @param node: The current node
        @param child: The child node to caculate g(x) for
        @return none
        """
        child.g_val = node.g_val + 1

    def getCount(self):
        """
        Returns the PathPlanner's count member
        
        @param self: The PathPlanner object
        @return an integer value: the PathPlanner's count member
        """
        return self.count

    def expand_node(self, node, grid):
        """
        Given a grid environment and a node, set the node's list of children according to 
        the moves (DOWN, RIGHT, UP, LEFT) that are available at that node's position in the grid.
        
        @param self: The PathPlanner object
        @param node: The node to expand
        @param grid: A 2D array representing the environment in which the search takes place
        @return none
        """
        
        i = node.getX()
        j = node.getY()

        if (i != self.Nrows-1) and (grid[i+1][j] == 0):   # Down
            child = Node(i+1, j, node)
        if (j != self.Ncols-1) and (grid[i][j+1] == 0):   # Right
            child = Node(i, j+1, node)
        if (i != 0) and (grid[i-1][j] == 0):              # Up
            child = Node(i-1, j, node)
        if (j != 0) and (grid[i][j-1] == 0):              # Left
            child = Node(i, j-1, node)

    def breadth_first_search(self, start, goal, grid):
        """
        Given a grid environment, return True if a valid path
        from start to goal is found using BFS.
        
        @param self: The PathPlanner object
        @param start: The node to begin search at.
        @param goal: The node being searched for.
        @param grid: A 2D array representing the environment in which the search takes place.
        @return True if a path was found, False otherwise
        """
        
        path_found = False
        coordinate = str(start.getX()) + ", " + str(start.getY())
        coordinate = coordinate.replace(" ", "")
        coordinate = coordinate.replace(",", ", ")

        # Set current node (start) as visited and add to stack
        self.queue.append(start)
        self.visited_str.append(coordinate)

        while (self.queue != []):
            node = self.queue.pop(0)
            
            self.count += 1
            if (node.getX() == goal.getX() and node.getY() == goal.getY()):
                path_found = True
                break

            self.expand_node(node, grid)

            for i in range(0, len(node.children)) :
                coordinate = str(node.children[i].getX()) + ", " + str(node.children[i].getY())
                coordinate = coordinate.replace(" ", "")
                coordinate = coordinate.replace(",", ", ")
                if coordinate not in self.visited_str :
                    self.queue.append(node.children[i])
                    self.visited_str.append(coordinate)

        if not path_found:
            return False
        
        # Build path backwards using parent links
        self.visited_str = []
        coordinate = str(node.getX()) + ", " + str(node.getY())
        coordinate = coordinate.replace(" ", "")
        coordinate = coordinate.replace(",", ", ")
        self.visited_str.insert(0, coordinate)
        while (1):
            coordinate = str(node.parent.getX()) + ", " + str(node.parent.getY())
            coordinate = coordinate.replace(" ", "")
            coordinate = coordinate.replace(",", ", ")
            self.visited_str.insert(0, coordinate)
            node = node.parent
            if (node.getX() == start.getX()) and (node.getY() == start.getY()) :
                return path_found

    def depth_first_search(self, start, goal, grid):
        """
        Given a grid environment, return True if a valid path
        from start to goal is found using a DFS.
        
        @param self: The PathPlanner object
        @param start: The node to begin search at.
        @param goal: The node being searched for.
        @param grid: A 2D array representing the environment in which the search takes place.
        @return True if a path was found, False otherwise
        """
        
        path_found = False
        self.stack.append(start)
        limit = -1

        while (self.stack != []) :
            limit += 1

            for i in range(0, 2**limit):
                for j in reversed(self.stack):
                    node = j
                    if (node.height > limit):
                        continue
                    else:
                        self.stack.remove(node)
                        break
                
                coordinate = str(node.getX()) + ", " + str(node.getY())
                coordinate = coordinate.replace(" ", "")
                coordinate = coordinate.replace(",", ", ")
                self.visited_str.append(coordinate)

                self.expand_node(node, grid)
                for i in range(0, len(node.children)):
                    self.count += 1
                    if (node.children[i].getX() == goal.getX() and node.children[i].getY() == goal.getY()) :
                        path_found = True
                        node = node.children[i]
                        break

                    coordinate = str(node.children[i].getX()) + ", " + str(node.children[i].getY())
                    coordinate = coordinate.replace(" ", "")
                    coordinate = coordinate.replace(",", ", ")
                
                    if coordinate not in self.visited_str:
                        self.stack.append(node.children[i])

                if path_found:
                    break

            if path_found:
                # Build path backwards using parent links
                self.visited_str = []
                coordinate = str(node.getX()) + ", " + str(node.getY())
                coordinate = coordinate.replace(" ", "")
                coordinate = coordinate.replace(",", ", ")
                self.visited_str.insert(0, coordinate)
                while (1):
                    coordinate = str(node.parent.getX()) + ", " + str(node.parent.getY())
                    coordinate = coordinate.replace(" ", "")
                    coordinate = coordinate.replace(",", ", ")
                    self.visited_str.insert(0, coordinate)
                    node = node.parent
                    if (node.getX() == start.getX()) and (node.getY() == start.getY()) :
                        return path_found

        if not path_found:
            return False

    def a_star_search(self, start, goal, grid):
        """
        Given a grid environment, return True if a valid path
        from start to goal is found using an A* search.
        
        @param self: The PathPlanner object
        @param start: The node to begin search at.
        @param goal: The node being searched for.
        @param grid: A 2D array representing the environment in which the search takes place.
        @return True if a path was found, False otherwise
        """

        path_found = False
        # Set h(x) and g(x) for start node
        self.calculate_hx(start, goal) 
        start.g_val = 0

        open = []
        open.append(start)
        closed = []

        while (open != []):            
            # Find node with least f
            f1 = 10000
            for i in range(0, len(open)):
                f2 = open[i].getH_val() + open[i].getG_val()
                if (f2 < f1):
                    f1 = f2
                    node = open[i]
            
            open.remove(node)
            self.expand_node(node, grid)
            self.count += 1
            
            for i in range(0, len(node.children)) :
                skip_child = False
                child = node.children[i]
                if (child.getX() == goal.getX() and child.getY() == goal.getY()) :
                    path_found = True
                    break

                for i in range(0, len(closed)):
                    if (closed[i].getX() == child.getX() and closed[i].getY() == child.getY()):
                        skip_child = True
                        break
                if skip_child:
                    continue
                
                # For each child, calculate f(x) = h(x) + g(x)
                self.calculate_gx(node, child)
                self.calculate_hx(child, goal)
                f = child.getH_val() + child.getG_val()

                for i in range(0, len(open)):
                    if (open[i].getX() == child.getX() and open[i].getY() == child.getY()):
                        if (child.getG_val() >= open[i].getG_val()):
                            skip_child = True
                            break
                if skip_child:
                    continue
                else:
                    open.append(child)
            
            closed.append(node)

            if path_found:
                coordinate = str(goal.getX()) + ", " + str(goal.getY())
                coordinate = coordinate.replace(" ", "")
                coordinate = coordinate.replace(",", ", ")
                
                self.visited_str.insert(0, coordinate)
                while True:
                    coordinate = str(node.getX()) + ", " + str(node.getY())
                    coordinate = coordinate.replace(" ", "")
                    coordinate = coordinate.replace(",", ", ")
                    
                    self.visited_str.insert(0, coordinate)
                    if (node.getX() == start.getX() and node.getY() == start.getY()):
                        return path_found
                    
                    node = node.parent
        
        return path_found

def main():
    """
    Given a file containing the specifications of a grid environment, a starting coordinate,
    a goal coordinate, and a specified search method, find the shortest path from the
    starting coordinate to the goal using the specified search method and print the results.
    
    @return 0 at end of process
    """

    if (len(sys.argv) != 9):
        sys.exit("Usage: python main.py --input FILENAME --start START_NODE --goal GOAL_NODE --search SEARCH_TYPE")

    if (sys.argv[1] != "--input" or sys.argv[3] != "--start" or sys.argv[5] != "--goal" or sys.argv[7] != "--search"):
        sys.exit("Usage: python main.py --input FILENAME --start START_NODE --goal GOAL_NODE --search SEARCH_TYPE")

    start = sys.argv[4]
    end = sys.argv[6]
    search_type = sys.argv[8]

    # Read file
    with open(sys.argv[2], 'r') as file:
        Nrows = 0
        grid = []
        gridline = []

        for line in file:
            Nrows += 1
            Ncols = 0
            for i in line:
                if (i == '0'):
                    gridline.append(0)
                    Ncols += 1          
                elif (i == '1'):
                    gridline.append(1)
                    Ncols += 1
                elif (i == ','):
                    continue
                elif (i == '\n'):
                    break
                else:
                    sys.exit("File contains invalid character")
            grid.append(gridline)
            gridline = []
    file.close()

    # Check for valid Start coordinate
    coordinate = start.split(',')
    if (len(coordinate) == 2 and coordinate[0].isnumeric() and coordinate[1].isnumeric()):
        if (int(coordinate[0]) >= Nrows or int(coordinate[1]) >= Ncols):
            sys.exit("START_NODE is outside the grid environment")
        if (grid[int(coordinate[0])][int(coordinate[1])] == 1):
            sys.exit("START_NODE invalid: obstacle in the way.")
    else:
        print("START_NODE and GOAL_NODE must be in coordinate form.")
        sys.exit("Usage: python main.py --input FILENAME --start START_NODE --goal GOAL_NODE --search SEARCH_TYPE")

    root = Node(coordinate[0], coordinate[1])

    # Check for valid Goal coordinate
    coordinate = end.split(',')
    if (len(coordinate) == 2 and coordinate[0].isnumeric() and coordinate[1].isnumeric()):
        if (int(coordinate[0]) >= Nrows or int(coordinate[1]) >= Ncols):
            sys.exit("GOAL_NODE is outside the grid environment")
        if (grid[int(coordinate[0])][int(coordinate[1])] == 1):
            sys.exit("GOAL_NODE invalid: obstacle in the way.")
    else:
        print("START_NODE and GOAL_NODE must be in coordinate form.")
        sys.exit("Usage: python main.py --input FILENAME --start START_NODE --goal GOAL_NODE --search SEARCH_TYPE")

    goal = Node(coordinate[0], coordinate[1])

    if (root.getX() == goal.getX() and root.getY() == goal.getY()):
        sys.exit("GOAL_NODE is the START_NODE, no need to search")

    # Instansiate PathPlanner Object and Carry out Search
    PathPlan = PathPlanner(Nrows, Ncols)
    if (search_type == "BFS"):
        path_found = PathPlan.breadth_first_search(root, goal, grid)

    elif (search_type == "DFS"): 
        path_found = PathPlan.depth_first_search(root, goal, grid)

    elif (search_type == "A*"):
        path_found = PathPlan.a_star_search(root, goal, grid)

    elif (search_type == "ALL"):
        bfs_path = PathPlan.breadth_first_search(root, goal, grid)
        if bfs_path:
            # Print out path and number of nodes traversed
            print("Path: " + '[', end='')
            for i in range(0, len(PathPlan.visited_str)):
                if i == len(PathPlan.visited_str)-1 :
                    print('(' + PathPlan.visited_str[i], end=')]')
                    break
                print('(' + PathPlan.visited_str[i], end='), ')
            print("\nTraversed:", PathPlan.getCount())
        else:
            sys.exit("Path could not be found.")

        PathPlan.count = 0
        PathPlan.visited_str = []
        dfs_path = PathPlan.depth_first_search(root, goal, grid)
        if dfs_path:
            # Print out path and number of nodes traversed
            print("Path: " + '[', end='')
            for i in range(0, len(PathPlan.visited_str)):
                if i == len(PathPlan.visited_str)-1 :
                    print('(' + PathPlan.visited_str[i], end=')]')
                    break
                print('(' + PathPlan.visited_str[i], end='), ')
            print("\nTraversed:", PathPlan.getCount())
        else:
            sys.exit("Path could not be found")
        
        PathPlan.count = 0
        PathPlan.visited_str = []
        astar_path = PathPlan.a_star_search(root, goal, grid)
        # Print out path and number of nodes traversed
        print("Path: " + '[', end='')
        for i in range(0, len(PathPlan.visited_str)):
            if i == len(PathPlan.visited_str)-1 :
                print('(' + PathPlan.visited_str[i], end=')]')
                break
            print('(' + PathPlan.visited_str[i], end='), ')
        print("\nTraversed:", PathPlan.getCount())
        return 0

    else:
        print("Invalid SEARCH_TYPE...")
        sys.exit("Options are: BFS | DFS | A* | ALL")

    if not path_found:
        sys.exit("Could not find a path.")
        
    # Print out path and number of nodes traversed
    print("Path: " + '[', end='')
    for i in range(0, len(PathPlan.visited_str)):
        if i == len(PathPlan.visited_str)-1 :
            print('(' + PathPlan.visited_str[i], end=')]')
            break
        print('(' + PathPlan.visited_str[i], end='), ')
    print("\nTraversed:", PathPlan.getCount())

    return 0

if __name__ == '__main__':
    main()
