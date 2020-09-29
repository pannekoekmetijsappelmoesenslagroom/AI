import itertools

"""
a) 
    1) Er zijn 8 kaarten te plaatsen op de 8 posities dus 8! mogelijke permutaties.
       Hierbij gaan we er dus van uit dat twee kaarte net het zelfde symbool niet het zelfde zijn maar van kleur verschillen en dus uniek. 

    2) de eerste oplossing si bij permutatie 30

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

rules = [
    lambda conf: each_card_x_has_neighbor_y(conf, "a", "h") or each_card_x_has_neighbor_y(conf, "a", ""),
    lambda conf: each_card_x_has_neighbor_y(conf, "h", "d") or each_card_x_has_neighbor_y(conf, "h", ""),
    lambda conf: each_card_x_has_neighbor_y(conf, "d", "b") or each_card_x_has_neighbor_y(conf, "d", ""),
    lambda conf: not each_card_x_has_neighbor_y(conf, "a", "d"),
    lambda conf: not each_card_x_has_neighbor_y(conf, "a", "a"),
    lambda conf: not each_card_x_has_neighbor_y(conf, "h", "h"),
    lambda conf: not each_card_x_has_neighbor_y(conf, "d", "d"),
    lambda conf: not each_card_x_has_neighbor_y(conf, "b", "b"),
]

def comform_all_rules(rules, configuration):
    for rule in rules:
        if rule(configuration) == False:
            return False
    return True

for i, configuration in enumerate(itertools.permutations('aAhHdDbB')):
    if comform_all_rules(rules, configuration):
        print("permutatie:", i, configuration)
        break



# config = 8*[""]
# counter = 0
# print(config)
# def dfs(index=0):
#     global counter
#     counter += 1
#     if index == 8:
#         print(config)
#         return
#     for v in ["a","A","h","H","d","D","b","B"]:
#         config[index] = v;
#         if comform_all_rules(rules, config):
#             dfs(index+1)
#     config[index] = "";

# dfs()
# print(counter)
