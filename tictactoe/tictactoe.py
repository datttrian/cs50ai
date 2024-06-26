"""
Tic Tac Toe Player
"""

X = "X"
O = "O"  # noqa: E741
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
    Returns the best move for the current player on the board.
    """
    current_player = player(board)

    if terminal(board):
        return None

    if current_player == X:
        best_move = None
        best_score = float("-inf")
        for action in actions(board):
            score = min_value(result(board, action))
            if score > best_score:
                best_score = score
                best_move = action
        return best_move

    best_move = None
    best_score = float("inf")
    for action in actions(board):
        score = max_value(result(board, action))
        if score < best_score:
            best_score = score
            best_move = action
    return best_move


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
