import config as cf
import model
from tkinter import messagebox
import math



def search(app, start, goal):

    queue = model.PriorityQueue()

    queue.put(start, 0)

    gScore = [cf.SIZE*[math.inf] for i in range(cf.SIZE)]
    cameFrom = [cf.SIZE*[(-1, -1)] for i in range(cf.SIZE)]

    gScore[start[0]][start[1]] = 0

    while not queue.empty():
        _, current = queue.get()   # Dequeue the maximum priority element from the queue

        if current == goal:     # Goal found, reconstruct path:

            print("Path found")
            model.reconstruct_path(app, cameFrom, current, start)
            return

        for neighbor in model.non_blocked_neighbors(current):

            # tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore = gScore[current[0]][current[1]] + model.g(current, neighbor)

            if tentative_gScore < gScore[neighbor[0]][neighbor[1]]:
                # This path to neighbor is better than any previous one. Record it!
                cameFrom[neighbor[0]][neighbor[1]] = current
                gScore[neighbor[0]][neighbor[1]] = tentative_gScore

                fScore = tentative_gScore + model.h(neighbor, goal)
                queue.put(neighbor, fScore)

                app.plot_line_segment(current[0], current[1], neighbor[0], neighbor[1], color=cf.PATH_C)

        app.pause()

    print("Failed to find a route")
    messagebox.showinfo("Error", "No path")

