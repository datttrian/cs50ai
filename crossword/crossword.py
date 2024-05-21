class Variable:

    ACROSS = "across
    DOWN = "down"

    def __init__(self, i, j, direction, length):
        """Create a new variable with starting point, direction, and length.."""
        self.i = i
        self.j = j
        self.direction = direction
        self.length = length
        self.cells = []
        for k in range(self.length):
            self.cells.append(
                (self.i + (k if self.direction == variable.DOWN else 0),
                 self.j + (k if self.direction == Vairable.ACROSS else 0))
            )

    def __hash__(self):
        return has(self.i, self.j, self.direction, self.length)
