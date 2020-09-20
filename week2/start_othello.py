"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a 100-element list, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`. This is because size of square is 10x10,
   and mn means m*10 + n. This avoids conversion between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""

# The outside edge is marked ?, empty squares are ., black is @, and white is o.
# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11

# 8 directions; note UP_LEFT = -11, we can repeat this from row to row
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

def squares():
    # list all the valid squares on the board.
    # returns a list [11, 12, 13, 14, 15, 16, 17, 18, 21, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
    # PRINT a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    print(rep)
    # return rep

# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. # A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()  # todo: `move in squares()` is an expensive thing to check

def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE

def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with `square` for `player` in the given
    # `direction`
    # returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be is an occupied line in some direction
    # any(iterable) : Return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)

# Making moves
# When the player makes a move, we need to update the board and flip all the
# bracketed pieces.

def make_move(move, player, board):
    # update the board to reflect the move by the specified player
    # assuming now that the move is valid
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction

# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board
    
    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

def legal_moves(player, board):
    # get a list of all legal moves for player
    # legals means : move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())

# Putting it all together

# Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def play(black_strategy, white_strategy):
    # play a game of Othello and return the final board and score

    board = initial_board()
    curr_player = BLACK

    print("Initial board:")
    print_board(board)

    while True:

        strategy = black_strategy if curr_player is BLACK else white_strategy
        
        print('%s turn' % PLAYERS[curr_player])

        proposed_move = get_move(strategy, curr_player, board)

        make_move(proposed_move, curr_player, board)

        print_board(board)
        print('%s did move %d' % (PLAYERS[curr_player], proposed_move))
        
        curr_player = next_player(board, curr_player)
        if curr_player is None:
            break   # game is done

    for player, name in PLAYERS.items():
        print('%s score: %d' % (name, score(player, board)))

    return board

def next_player(board, prev_player):
    # which player should move next?  Returns None if no legal moves exist
    if any_legal_move(opponent(prev_player), board):
        return opponent(prev_player)
    
    elif any_legal_move(prev_player, board):
        return prev_player

    return None

def get_move(strategy, player, board):
    # call strategy(player, board) to get a move
    move = strategy(player, board)
    if not is_legal(move, player, board) or not is_valid(move):
        raise IllegalMoveError(player, move, board)
    return move


def score(player, board):
    # compute player's score (number of player's pieces minus opponent's)
    score = 0
    for sq in board:
        if sq is player:
            score = score + 1
        elif sq is opponent(player):
            score = score - 1
    return score

# Play strategies
def cli_strategy(player, board):
    print("legal moves: ", legal_moves(player, board))
    return int(input("Your input: "))


import random

def random_strategy(player, board):
    return random.choice(legal_moves(player, board))

import math

def negamax(node, depth, player_val, heuristic, get_children, alpha, beta):

    children = get_children(node, player_val)

    value = -math.inf
    best = node

    if depth == 0 or len(children) == 0:
        value = player_val * heuristic(node)
    
    else:
        for child in children:
            score, _ = negamax(child, depth - 1, -player_val, heuristic, get_children, -beta, -alpha)
            score = score * -1

            if score > value:
                best = child
                value = score

            alpha = max(alpha, value)
            if alpha >= beta:
                break

    return value, best


def get_board_with_magic_scores():
    magic_scores = [
        1.010000 	,-0.270000 	,0.560000 	,-0.253853 	,-0.253853 	,0.560000 	,-0.270000 	,1.010000,
        -0.270000 	,-0.740000 	,-0.384101 	,-0.080000 	,-0.080000 	,-0.384101 	,-0.740000 	,-0.270000,
        0.560000 	,-0.384101 	,-0.239954 	,-0.155662 	,-0.155662 	,-0.239954 	,-0.384101 	,0.560000,
        -0.253853 	,-0.080000 	,-0.155662 	,-0.010000 	,-0.010000 	,-0.155662 	,-0.080000 	,-0.253853,
        -0.253853 	,-0.080000 	,-0.155662 	,-0.010000 	,-0.010000 	,-0.155662 	,-0.080000 	,-0.253853,
        0.560000 	,-0.384101 	,-0.239954 	,-0.155662 	,-0.155662 	,-0.239954 	,-0.384101 	,0.560000,
        -0.270000 	,-0.740000 	,-0.384101 	,-0.080000 	,-0.080000 	,-0.384101 	,-0.740000 	,-0.270000,
        1.010000 	,-0.270000 	,0.560000 	,-0.253853 	,-0.253853 	,0.560000 	,-0.270000 	,1.010000,
    ]
    assert(len(magic_scores) is len(squares()))

    magic_scores_board = initial_board()

    i = 0
    for sq in squares():
        magic_scores_board[sq] = magic_scores[i]
        i = i + 1

    assert(magic_scores_board[11] == magic_scores[0])
    assert(magic_scores_board[88] == magic_scores[63])

    return magic_scores_board


def negamax_strategy(player, board):

    max_depth = 7

    magic_scores_board = get_board_with_magic_scores()

    class Node:
        def __init__(self, move, tempBoard):
            self.move = move
            self.tempBoard = tempBoard

    def heuristic(node):
        return score(player, node.tempBoard)

    def magic_heuristic(node):

        score = 0
        for sq in squares():
            if node.tempBoard[sq] is player:
                score = score + magic_scores_board[sq]

            if node.tempBoard[sq] is opponent(player):
                score = score - magic_scores_board[sq]

        return score

    def get_children(node, player_val):
        children = []

        curr_player = player if player_val == 1 else opponent(player)

        moves = legal_moves(curr_player, node.tempBoard)
        for move in moves:
            node = Node(move, node.tempBoard.copy())
            make_move(move, curr_player, node.tempBoard)
            children.append(node)

        return children


    _h, bestNode = negamax(Node(None, board), max_depth, 1, magic_heuristic, get_children, -math.inf, math.inf)

    assert(bestNode.move is not None)
    print(_h)

    return bestNode.move


play(random_strategy, negamax_strategy)
