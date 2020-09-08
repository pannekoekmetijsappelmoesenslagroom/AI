import random
import heapq
import math
import config as cf
from tkinter import messagebox

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
        return heapq.heappop(self.elements)[1]

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node.x][node.y]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node.x][node.y] = value


def reconstruct_path(app, cameFrom, current, start):
    total_path = [current]
    while current != start:
        nextCurrent = cameFrom[current.y][current.x]
        app.plot_line_segment(current.y, current.x, nextCurrent.y, nextCurrent.x, color=cf.FINAL_C)
        app.pause()
        current = nextCurrent


def neighbors_g(n):
    if n.y+1 <= cf.SIZE-1:  yield cf.Point(n.x,   n.y+1 )
    if n.x+1 <= cf.SIZE-1:  yield cf.Point(n.x+1, n.y   )
    if n.y-1 >= 0:          yield cf.Point(n.x,   n.y-1 )
    if n.x-1 >= 0:          yield cf.Point(n.x-1, n.y   )

def g(n, start):
    return abs(n.x-start.x) + abs(n.y-start.y)

def h(n, goal):
    return math.sqrt((n.x-goal.x)**2 + (n.y-goal.y)**2)

def search(app, start, goal, use_h):
    openSet = PriorityQueue()
    openSet.put(start, 1) 

    cameFrom = [cf.SIZE*[0] for i in range(cf.SIZE)]

    checkedlist = [cf.SIZE*[0] for i in range(cf.SIZE)]
    checkedlist[start.y][start.x] = 1

    while not openSet.empty():
        current = openSet.get()
        if current == goal:
            reconstruct_path(app, cameFrom, current, start)
            return 
        
        for neighbor in neighbors_g(current):
            if g(current, start) < g(neighbor, start):
                cameFrom[neighbor.y][neighbor.x] = current
                if checkedlist[neighbor.y][neighbor.x] == 0 and grid[neighbor.y][neighbor.x] != 'b':
                    checkedlist[neighbor.y][neighbor.x] = 1
                    
                    app.plot_line_segment(current.y, current.x, neighbor.y, neighbor.x, color=cf.PATH_C)
                    app.pause()
                    
                    if use_h:
                        openSet.put(neighbor, h(neighbor, goal))
                    else:
                        openSet.put(neighbor, 1)

    print("Failed to find a route")
    messagebox.showinfo("Error", "No path")

