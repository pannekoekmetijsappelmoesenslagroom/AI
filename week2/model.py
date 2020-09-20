import random
import itertools
import math
from copy import copy, deepcopy

MAX_DEPTH = 3

def merge_left(b):
    # merge the board left
    # this is the funcyoin that is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left

        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accumulator
        if len(row) == 1:
            return acc + [x]

        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accumulator, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accumulator, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]


def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]


def merge_down(b):
    # merge the board downward
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[0, 0, 0, 2], [0, 0, 2, 4], [0, 0, 8, 2], [4, 8, 4, 2]]
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]


# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}

def move_exists(b):


    for move in MERGE_FUNCTIONS.keys():
        b = MERGE_FUNCTIONS[move](b)

    for i in range(4):
        for j in range(4):
            if b[i][j] == 0:
                return True
    return False

    # # check whether or not a move exists on the board
    # # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # # move_exists(b) return False
    # def inner(b):
    #     for row in b:
    #         for x, y in zip(row[:-1], row[1:]):
    #             # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
    #             if x == y or x == 0 or y == 0:
    #                 return True
    #     return False

    # if inner(b) or inner(zip(*b)):
    #     return True
    # else:
    #     return False

def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b


def play_move(b, direction):
    # get merge functin an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b


def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, rows):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue

def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [(2, 4, 8, 4), (0, 2, 2, 8), (0, 0, 0, 4), (0, 0, 0, 2)]
    assert merge_down(b) == [(0, 0, 0, 4), (0, 0, 0, 8), (0, 2, 8, 4), (2, 4, 2, 2)]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [(2, 8, 4, 0), (16, 0, 2, 0), (4, 0, 0, 0), (0, 0, 0, 0)]
    assert (merge_down(b)) == [(0, 0, 0, 0), (2, 0, 0, 0), (16, 0, 4, 0), (4, 8, 2, 0)]
    assert (move_exists(b)) == True
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    g = Game()
    for i in range(11):
        g.add_two_four(b)

def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))


class Node:
    def __init__(self, move, tempBoard, probability=-1):
        self.move = move
        self.tempBoard = tempBoard
        self.probability = probability

def expectimax(node, depth, player_val, heuristic, get_children):

    children = get_children(node, player_val)

    value = -math.inf
    best = node

    if depth == 0 or len(children) == 0:
        value = heuristic(node)

    elif player_val == 1:
        for child in children:
            score, _ = expectimax(child, depth - 1, -1, heuristic, get_children)
            if score >= value:
                value = score
                best = child

    else:
        value = 0
        for child in children:
            score, _ = expectimax(child, depth - 1, 1, heuristic, get_children)
            value = value + child.probability * score

    return value, best


def get_expectimax_move(b):
    
    max_depth = 4

    def get_children(node, player_val):

        children = []

        if player_val == 1:
            # player

            if not move_exists(node.tempBoard):
                return []

            for move in MERGE_FUNCTIONS.keys():
                new_node = Node(move, deepcopy(node.tempBoard))
                new_node.tempBoard = MERGE_FUNCTIONS[move](new_node.tempBoard)
                children.append(new_node)

        else:
            # random 2 or 4

            open_tiles = 0

            for i in range(4):
                for j in range(4):
                    if node.tempBoard[i][j] != 0:
                        continue

                    open_tiles = open_tiles + 1

                    node2 = Node(None, deepcopy(node.tempBoard), .9)
                    node2.tempBoard[i][j] = 2

                    node4 = Node(None, deepcopy(node.tempBoard), .1)
                    node4.tempBoard[i][j] = 4

                    children.append(node2)
                    children.append(node4)

            for child in children:
                child.probability = child.probability / open_tiles

        return children

    def heuristic(node):

        open_tiles = 0
        score = 0

        for i in range(4):
            for j in range(4):

                val = node.tempBoard[i][j]

                if val == 0:
                    open_tiles = open_tiles + 1

                if i % 3 == 0:
                    val = val * 4

                if j % 3 == 0:
                    val = val * 4

                score = score + val
        
        if score == 2048:
            return math.inf

        return open_tiles + score * .01
    
    _, bestNode = expectimax(Node(None, b), max_depth, 1, heuristic, get_children)

    assert(bestNode.move is not None)

    print(bestNode.move)

    return bestNode.move



