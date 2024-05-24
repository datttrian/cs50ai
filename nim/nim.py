import math
import random
import time


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        """
        Initialize game board.
        Each game board has
            - `piles`: a list of how many elements remain in each pile
            - `player`: 0 or 1 to indicate which player's turn
            - `winner`: None, 0, or 1 to indicate who the winner is
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Nim.available_actions(piles) takes a `piles` list as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of removing `j` items
        from pile `i` (where piles are 0-indexed).
        """
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Nim.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count
        self.switch_player()

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


# Instantiate the game
game = Nim()

print("Initial Piles:", game.piles)
print("Current Player:", game.player)

# Define some actions to perform
actions = [(0, 1), (1, 2), (2, 1), (3, 3)]

# Perform the actions
for action in actions:
    try:
        print(f"Player {game.player} takes {action[1]} from pile {action[0]}")
        game.move(action)
        print("Piles after move:", game.piles)
        print("Next Player:", game.player)
        if game.winner is not None:
            print(f"Winner: Player {game.winner}")
            break
    except Exception as e:
        print("Error:", e)


# Instantiate the game
game = Nim()

# Print the initial state
print("Initial Piles:", game.piles)

# Get available actions
actions = Nim.available_actions(game.piles)
print("Available Actions:", actions)


# Instantiate the game
game = Nim()

# Print the current player
print("Current Player:", game.player)

# Get the other player
other = Nim.other_player(game.player)
print("Other Player:", other)
