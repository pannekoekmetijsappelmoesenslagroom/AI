import config as cf
import model
from tkinter import messagebox

"""

algorithm explanation found on: https://www.geeksforgeeks.org/uniform-cost-search-dijkstra-for-large-graphs/

"""


def search(app, start, goal):

    queue = model.PriorityQueue()

    queue.put(start, 0)

    visited = [cf.SIZE*[False] for i in range(cf.SIZE)]
    cameFrom = [cf.SIZE*[(-1, -1)] for i in range(cf.SIZE)]

    while not queue.empty():
        currentCost, current = queue.get()   # Dequeue the maximum priority element from the queue

        if current == goal:     # Goal found, reconstruct path:

            print("Path found")
            model.reconstruct_path(app, cameFrom, current, start)
            return

        if not visited[current[0]][current[1]]:
            for neighbor in model.non_blocked_neighbors(current):    # Insert all the children of the dequeued element, with the cumulative costs as priority
                
                if visited[neighbor[0]][neighbor[1]]:
                    continue

                app.plot_line_segment(current[0], current[1], neighbor[0], neighbor[1], color=cf.PATH_C)
                
                cameFrom[neighbor[0]][neighbor[1]] = current
                queue.put(neighbor, model.g(neighbor, start) + currentCost)

        visited[current[0]][current[1]] = True
        app.pause()
    
    print("Failed to find a route")
    messagebox.showinfo("Error", "No path")

