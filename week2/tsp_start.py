"""

A)
    NN:       10 city tour with length 2989.1 in 0.000 secs for try_nn
    Try all:  10 city tour with length 2811.5 in 1.952 secs for try_all_tours

    2989.1 / (2811.5 / 100) - 100 ~= 6.3   So NN gives with seed 17701 and 10 cities a 6% less optimal route

B)  NN gives with seed 17701 and 500 cities the following result:
    500 city tour with length 20445.9 in 0.049 secs for try_nn

C)  N steden heeft als route een route met N-1 takken / wegen

    Er zijn veel verschillende manieren hoe je kruisende takken / wegen kan vinden maar dit op een snelle manier doen is moeilijk, 
    Het komt er meestal op neer dat je iedere lijn segment met ieder andere lijn segment zal moeten controleren. 
    Dit is nog iets te versnellen de zoektocht te beginnen vanaf de buren. 
    Een heel naive manier is door AABB te gebruiken of om bounding boxes te gebruiken en zo zijn er nog vele andere manieren. 
    De manier die wij handig zouden kunnen gebruiken is het geval waar we een bruising omdraaien. Als de route dan korter word houden we de aanpassing.

    Als een kruising gevonden is kan door het slim rond draaien van de steden in de route altijd een kortere route gevonden worden.

D)  Op de manier hou wij het geimplementeerd hebben O(n^2)
"""
import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]

def try_nn(cities):
    city_list = list(cities)[:-1]
    result = [next(iter(cities))]
    city_list.remove(result[0])
    while len(city_list) > 0:
        nearest_length = math.inf
        nearest_city = None
        for city in city_list:
            d = distance(city, result[-1])
            if (nearest_length > d):
                nearest_length = d 
                nearest_city = city
        
        city_list.remove(nearest_city)
        result.append(nearest_city)

    return result

import numpy as np

# this is based on http://pedrohfsd.com/2017/08/09/2opt-part1.html
def try_two_opt(cities):
    route = list(cities)[:-1]
    best_route = route
    has_improved = True
    while has_improved:
        has_improved = False
        for i in range(1, len(route)-2):
            for j in range(i+2, len(route)):
                new_route = route[:]
                new_route[i:j] = route[j-1:i-1:-1]
                if tour_length(new_route) < tour_length(best_route):
                    best_route = new_route
                    has_improved = True
        route = best_route
    return best_route

def try_two_opt_naive(cities):
    route = list(cities)[:-1]

    for a_index, a in enumerate(route):
        for cIndex, c in enumerate(route):
            if (a_index != cIndex) and a_index+1 < len(route) and cIndex+1<len(route):
                a1 = distance(a, route[a_index+1])
                b1 = distance(c, route[cIndex+1])

                a2 = distance(a, route[cIndex+1])
                b2 = distance(c, route[a_index+1])
                if (a2 + b2 < a1 + b1):
                    route[a_index+1], route[cIndex+1] = route[cIndex+1], route[a_index+1]  

    return route

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(17701) # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.clock()
    tour = algorithm(cities)
    t1 = time.clock()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)
    
plot_tsp(try_nn, make_cities(10))
