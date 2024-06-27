"""
Tic Tac Toe Player
"""

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if not (0 <= i < 3 and 0 <= j < 3):
        raise ValueError("Action out of bounds")

    if board[i][j] is not EMPTY:
        raise ValueError("Invalid action")

    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(
        cell is not EMPTY for row in board for cell in row
    )


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    if winner_player == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)

    if terminal(board):
        return None

    if current_player == X:
        return max(actions(board), key=lambda action: min_value(result(board, action)))

    return min(actions(board), key=lambda action: max_value(result(board, action)))


def max_value(board):
    if terminal(board):
        return utility(board)

    v = float("-inf")

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = float("inf")

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def print_board(board):
    for row in board:
        print(" | ".join(cell if cell else " " for cell in row))
        print("---------")
    print()


def get_player_move(board):
    while True:
        try:
            move = input("Enter your move (row, col): ")
            i, j = map(int, move.split(","))
            action = (i, j)
            if action in actions(board):
                return action
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter row and column as integers separated by comma.")


board = initial_state()
print("Welcome to Tic Tac Toe!")

while not terminal(board):
    current_player = player(board)

    if current_player == X:
        print("\nPlayer X's turn")
        print_board(board)
        action = get_player_move(board)
    else:
        print("\nPlayer O is thinking...")
        action = minimax(board)

    board = result(board, action)

print_board(board)
print("\nGAME OVER")

game_winner = winner(board)
if game_winner:
    print(f"Player {game_winner} wins!")
else:
    print("It's a tie!")
