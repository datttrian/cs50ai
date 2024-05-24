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


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        state_tuple = tuple(state)
        return self.q.get((state_tuple, action), 0)

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        new_value_estimate = reward + future_rewards
        self.q[(tuple(state), action)] = old_q + self.alpha * (new_value_estimate - old_q)

    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        state_tuple = tuple(state)
        available_actions = Nim.available_actions(state)
        if not available_actions:
            return 0

        best_reward = 0
        for action in available_actions:
            q_value = self.q.get((state_tuple, action), 0)
            if q_value > best_reward:
                best_reward = q_value

        return best_reward

    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        available_actions = list(Nim.available_actions(state))
        if not available_actions:
            return None

        if epsilon and random.random() < self.epsilon:
            return random.choice(available_actions)
        else:
            state_tuple = tuple(state)
            best_action = None
            best_q_value = float('-inf')
            for action in available_actions:
                q_value = self.q.get((state_tuple, action), 0)
                if q_value > best_q_value:
                    best_q_value = q_value
                    best_action = action

            return best_action if best_action is not None else random.choice(available_actions)


# Initialize the game
game = Nim()

# Print the initial state
print("Initial state:", game.piles)

# Perform some actions manually
actions = [(0, 1), (1, 1), (2, 3), (3, 7)]
for action in actions:
    print(f"Player {game.player} performs action: {action}")
    game.move(action)
    print("Current state:", game.piles)
    if game.winner is not None:
        print(f"Player {game.winner} wins!")
        break

# Reset the game
print()
game = Nim()

# Initialize the AI
ai = NimAI()

# Perform actions using the AI
while game.winner is None:
    state = game.piles.copy()
    action = ai.choose_action(state, epsilon=False)
    print(f"Player {game.player} (AI) performs action: {action}")
    game.move(action)
    print("Current state:", game.piles)
    if game.winner is not None:
        print(f"Player {game.winner} wins!")
