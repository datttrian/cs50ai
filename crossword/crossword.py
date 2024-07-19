class Variable:

    ACROSS = "across"
    DOWN = "down"

    def __init__(self, i, j, direction, length):
        """Create a new variable with starting point, direction, and length."""
        self.i = i
        self.j = j
        self.direction = direction
        self.length = length
        self.cells = []
        for k in range(self.length):
            self.cells.append(
                (
                    self.i + (k if self.direction == Variable.DOWN else 0),
                    self.j + (k if self.direction == Variable.ACROSS else 0),
                )
            )

    def __hash__(self):
        return hash((self.i, self.j, self.direction, self.length))

    def __eq__(self, other):
        return (
            (self.i == other.i)
            and (self.j == other.j)
            and (self.direction == other.direction)
            and (self.length == other.length)
        )

    def __str__(self):
        return f"({self.i}, {self.j}) {self.direction} : {self.length}"

    def __repr__(self):
        direction = repr(self.direction)
        return f"Variable({self.i}, {self.j}, {direction}, {self.length})"


class Crossword:

    def __init__(self, structure_file, words_file):
        self.load_structure(structure_file)
        self.load_words(words_file)
        self.determine_variables()
        self.compute_overlaps()

    def load_structure(self, structure_file):
        """Load the structure of the crossword from a file."""
        with open(structure_file, encoding="utf-8") as f:
            contents = f.read().splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

            self.structure = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    if j >= len(contents[i]):
                        row.append(False)
                    elif contents[i][j] == "_":
                        row.append(True)
                    else:
                        row.append(False)
                self.structure.append(row)

    def load_words(self, words_file):
        """Load the vocabulary list from a file."""
        with open(words_file, encoding="utf-8") as f:
            self.words = set(f.read().upper().splitlines())

    def determine_variables(self):
        """Determine the set of variables in the crossword."""
        self.variables = set()
        for i in range(self.height):
            for j in range(self.width):
                self.add_vertical_variable(i, j)
                self.add_horizontal_variable(i, j)

    def add_vertical_variable(self, i, j):
        """Add a vertical variable starting at (i, j) if applicable."""
        if self.structure[i][j] and (i == 0 or not self.structure[i - 1][j]):
            length = 1
            for k in range(i + 1, self.height):
                if self.structure[k][j]:
                    length += 1
                else:
                    break
            if length > 1:
                self.variables.add(
                    Variable(i=i, j=j, direction=Variable.DOWN, length=length)
                )

    def add_horizontal_variable(self, i, j):
        """Add a horizontal variable starting at (i, j) if applicable."""
        if self.structure[i][j] and (j == 0 or not self.structure[i][j - 1]):
            length = 1
            for k in range(j + 1, self.width):
                if self.structure[i][k]:
                    length += 1
                else:
                    break
            if length > 1:
                self.variables.add(
                    Variable(i=i, j=j, direction=Variable.ACROSS, length=length)
                )

    def compute_overlaps(self):
        """Compute overlaps for each pair of variables."""
        self.overlaps = {}
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 == v2:
                    continue
                cells1 = v1.cells
                cells2 = v2.cells
                intersection = set(cells1).intersection(cells2)
                if not intersection:
                    self.overlaps[v1, v2] = None
                else:
                    intersection = intersection.pop()
                    self.overlaps[v1, v2] = (
                        cells1.index(intersection),
                        cells2.index(intersection),
                    )

    def neighbors(self, var):
        """Given a variable, return set of overlapping variables."""
        return set(v for v in self.variables if v != var and self.overlaps[v, var])
