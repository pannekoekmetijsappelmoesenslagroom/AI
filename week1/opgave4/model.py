import random
import heapq
import math
import config as cf
import uc_search
import a_star_search

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # to be use in the A* algorithm
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    # in a min-heap, the keys of parent nodes are less than or equal to those
    # of the children and the lowest key is in the root node
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value

def search(app, start, goal):
    if app.alg.get() == "UC":
        uc_search.search(app, start, goal)
    elif app.alg.get() == "A*":
        a_star_search.search(app, start, goal)


def reconstruct_path(app, cameFrom, current, start):
    total_path = [current]
    while current != start:
        nextCurrent = cameFrom[current[0]][current[1]]
        app.plot_line_segment(current[0], current[1], nextCurrent[0], nextCurrent[1], color=cf.FINAL_C)
        app.pause()
        current = nextCurrent

def non_blocked_neighbors(n):
    for nb in neighbors(n):
        if grid[n[0]][n[1]] != 'b':
            yield nb

def neighbors(n):
    if n[1]+1 <= cf.SIZE-1:  yield (n[0],   n[1]+1 )
    if n[0]+1 <= cf.SIZE-1:  yield (n[0]+1, n[1]   )
    if n[1]-1 >= 0:          yield (n[0],   n[1]-1 )
    if n[0]-1 >= 0:          yield (n[0]-1, n[1]   )

def g(n, start):
    return abs(n[0]-start[0]) + abs(n[1]-start[1])

def h(n, goal):
    return math.sqrt((n[0]-goal[0])**2 + (n[1]-goal[1])**2)

