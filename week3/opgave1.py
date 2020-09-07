import itertools

people = ["L", "M", "N", "E", "J"]
bovenste = len(people) -1
begane_grond = 0
rules = [
    lambda L,M,N,E,J: L != bovenste,
    lambda L,M,N,E,J: M != begane_grond,
    lambda L,M,N,E,J: N != bovenste and N != begane_grond,
    lambda L,M,N,E,J: E > M,
    lambda L,M,N,E,J: abs(J - N) > 1,
    lambda L,M,N,E,J: abs(N - M) > 1,
]

def comform_all_rules(rules, configuration):
    for rule in rules:
        if rule(*configuration) == False:
            return False
    return True


for configuration in list(itertools.permutations(range(len(people)))):
    if comform_all_rules(rules, configuration):
        print(configuration)