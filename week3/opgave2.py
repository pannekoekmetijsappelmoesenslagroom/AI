import itertools

"""
a) 
    1) Er zijn 8 kaarten te plaatsen op de 8 posities dus 8! mogelijke permutaties.
       Hierbij gaan we er dus van uit dat twee kaarte net het zelfde symbool niet het zelfde zijn maar van kleur verschillen en dus uniek. 

    2) de eerste oplossing si bij permutatie 30

b)

c) 
    Een (start) voorbeeld hoe je dat kan opschrijven is als volgt.
    Stel 5 is een Aas.
    3,4,6,7 kunnen geen A zijn vanwege [5]
    3,4,6,7 kunnen geen V zijn vanwege [4]
    dus 3,4,6,7 moet een H of B zijn
    er zijn maar 2xH en 2xB kaarten, dus 0,1,2 moet een A of V zijn
     
allowed
    b  b
    |\/|
    |/\|
    d  d
    |\/|
    |/\|  
    h  h
    |\/|
    |/\|
    a  a

not allowed
    b--b
  
 ---d--d---
 |        |
 |  h--h  |
 |        |
 ---a--a---
 |  \  /  |
 ----==----
"""

# De opdracht gaf aan dit met een dictionary te doen die een (key=index, value=kaart) heeft maar dat is precies het zelfde als een array vandaar deze implementatie
neighbors_lookup = [
    [3],
    [2],
    [1,3,4],
    [0,2,5],
    [2,5],
    [3,4,6,7],
    [5],
    [5],
]

def card_indexes_g(conf, card):
    for i, x in enumerate(conf):
        if x.lower() == card.lower():
            yield i

def has_neighbor_oftype(conf, index, type):
    for i in neighbors_lookup[index]:
        if conf[i].lower() == type:
            return True
    return False

def each_card_x_has_neighbor_y(conf, x, y):
    return all(list(map(has_neighbor_oftype, 8*[conf], card_indexes_g(conf, y), 8*[x])))
def each_card_x_does_not_neighbor_y(conf, x, y):
    return any(list(map(has_neighbor_oftype, 8*[conf], card_indexes_g(conf, y), 8*[x])))


rules = [
    lambda conf: each_card_x_has_neighbor_y(conf, "a", "h"),
    lambda conf: each_card_x_has_neighbor_y(conf, "h", "d"),
    lambda conf: each_card_x_has_neighbor_y(conf, "d", "b"),
    lambda conf: each_card_x_does_not_neighbor_y(conf, "a", "d"),
    lambda conf: (not each_card_x_has_neighbor_y(conf, "a", "a")),
    lambda conf: (not each_card_x_has_neighbor_y(conf, "h", "h")),
    lambda conf: (not each_card_x_has_neighbor_y(conf, "d", "d")),
    lambda conf: (not each_card_x_has_neighbor_y(conf, "b", "b")),
]

def conform_all_rules(rules, configuration):
    for rule in rules:
        if rule(configuration) == False:
            return False
    return True

##### a)

for i, configuration in enumerate(itertools.permutations('aAhHdDbB')):
    if conform_all_rules(rules, configuration):
        print("permutatie:", i, configuration)
        # break


##### b)

def no_rule_broken(config):
    for i, x in enumerate(config):
        for j in neighbors_lookup[i]:
            y = config[j]
            if ((x.lower() in ["a","d","h","b"] and x.lower() == y.lower())):
                return False
    return True


config = 8*[" "]
counter = 0

def dfs(index=0):
    global counter
    counter += 1
    if index == 8:
        if config[-1] != " " and len(set(config)) == 8 and conform_all_rules(rules, config): # if we move this to the no rule broken it is faster then the first implementation
            print("counter", config)
        return
    for v in ["a","A","h","H","d","D","b","B"]:
        config[index] = v;
        if no_rule_broken(config):
            dfs(index+1)
    config[index] = "";

dfs()
print(counter)
