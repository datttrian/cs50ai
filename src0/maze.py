import sys


class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    # Define the function that removes a node from the frontier and returns it.
    def remove(self):
        # Terminate the search if the frontier is empty, because this means that there is no
        # solution.
        if self.empty():
            raise IndexError("empty frontier")
        # Save the last item in the list (which is the newest node added)
        node = self.frontier[-1]
        # Save all the items on the list besides the last node (i.e. removing the last node)
        self.frontier = self.frontier[:-1]
        return node


class QueueFrontier(StackFrontier):

    # Define the function that removes a node from the frontier and returns it.
    def remove(self):
        # Terminate the search if the frontier is empty, because this means that there is no
        # solution.
        if self.empty():
            raise IndexError("empty frontier")
        # Save the oldest item on the list (which was the first one to be added)
        node = self.frontier[0]
        # Save all the items on the list besides the first one (i.e. removing the first node)
        self.frontier = self.frontier[1:]
        return node


class Maze:
    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename, encoding="utf-8") as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise ValueError("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise ValueError("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.dimensions = {
            "height": len(contents),
            "width": max(len(line) for line in contents),
        }
        self.positions = {"start": None, "goal": None}

        # Keep track of walls
        self.walls = []
        for i in range(self.dimensions["height"]):
            row = []
            for j in range(self.dimensions["width"]):
                try:
                    if contents[i][j] == "A":
                        self.positions["start"] = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.positions["goal"] = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize an empty explored set
        self.explored = set()

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.positions["start"]:
                    print("A", end="")
                elif (i, j) == self.positions["goal"]:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]

        result = []
        for action, (r, c) in candidates:
            if (
                0 <= r < self.dimensions["height"]
                and 0 <= c < self.dimensions["width"]
                and not self.walls[r][c]
            ):
                result.append((action, (r, c)))
        return result

    def solve(self):
        """Finds a solution to maze, if one exists."""
        # Initialize frontier to just the starting position
        start = Node(state=self.positions["start"], parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise RuntimeError("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.positions["goal"]:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
