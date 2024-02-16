"""
A* Search Solution to find shortest path from a start point to an end point in a maze,
    where '1's are the blockage and '0's are part of the path
At any point, can to any adjacent point or diagonally adjacent point.
"""

class Node():
    """Node class for A* Search"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node with initial values
    start_node = Node(None, start)
    end_node = Node(None, end)

    # Initialize both open and closed list
    open_list = [start_node]
    closed_list = []

    # Loop until you find the end
    while open_list:

        # Current node is the node with the lowest f value
        current_node = min(open_list, key=lambda x: x.f)
        open_list.remove(current_node)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        # Generate children
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Validate
            if not (0 <= node_position[0] < len(maze)) or not (0 <= node_position[1] < len(maze[0])) or maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Skip if node is closed
            if new_node in closed_list:
                continue

            # Calculate the f, g, and h values
            new_node.g = current_node.g + 1
            new_node.h = (end_node.position[0] - node_position[0]) ** 2 + (end_node.position[1] - node_position[1]) ** 2
            new_node.f = new_node.g + new_node.h

            # Skip if node is in open list and has higher g value
            if any(child == new_node and new_node.g > child.g for child in open_list):
                continue

            # Add the child to the open list
            open_list.append(new_node)

def main():

    maze = [[0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]

    start = (0, 0)
    end = (7, 6)

    path = astar(maze, start, end)
    print(path)


if __name__ == '__main__':
    main()



