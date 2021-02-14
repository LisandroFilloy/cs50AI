"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    dif = 0
    for i in range(3):
        for j in range(3):
            actual = board[i][j]
            if actual == X:
                dif += 1
            elif actual == O:
                dif -= 1

    if dif == 0:
        return X
    else:
        return O


def actions(board):
    res = []
    for i in range(3):
        for j in range(3):
            #If the position is empty we append it to the list of possible actions
            if board[i][j] == EMPTY:
                res.append((i,j))

    return res


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if board[action[0]][action[1]] != EMPTY:
        raise Exception

    newBoard = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

    #Deep copy of the board.
    for i in range(3):
        for j in range(3):
            if(action != (i,j)):
                newBoard[i][j] = board[i][j]
            else:
                newBoard[i][j] = player(board)

    return newBoard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Row winner
    for Player in [X,O]:
        for i in range(3):
                if board[i][0] == Player and board[i][1] == Player and board[i][2] == Player:
                    return Player

    #Column winner
    for Player in [X,O]:
        for i in range(3):
                if board[0][i] == Player and board[1][i] == Player and board[2][i] == Player:
                    return Player

    #Diagonal winner
    for Player in [X,O]:
        if board[0][0] == Player and board[1][1] == Player and board[2][2] == Player:
            return Player
        if board[2][0] == Player and board[1][1] == Player and board[0][2] == Player:
            return Player

    #No one won
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #There is a winner
    if winner(board) != None:
        return True

    #No more possible moves
    if len(actions(board)) == 0:
        return True

    #The game is not terminal
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #it only accepts terminal boards
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    Player = player(board)

    if terminal(board):
        return None

    if Player == X:
        moves = []
        for action in actions(board):
            moves.append((action, minPlay(result(board,action))))

        moves.sort(key = lambda x: x[1])
        return moves[-1][0]

    if Player == O:
        moves = []
        for action in actions(board):
            moves.append((action, maxPlay(result(board,action))))

        moves.sort(key = lambda x: x[1])

        return moves[0][0]


def maxPlay(board):
    if terminal(board):
        return utility(board)

    next = []
    for action in actions(board):
        next.append(minPlay(result(board, action)))

    return max(next)


def minPlay(board):
    if terminal(board):
        return utility(board)

    next = []

    for action in actions(board):
        next.append(maxPlay(result(board, action)))

    return min(next)

