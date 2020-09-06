import random

# Normal Tree implementation with the exception that leaves is a boolean instead of a seperate object
# _!_ no strict validation checks on input
class Tree():
    def __init__(self):
        self.children = 26*[None]   # Every char has one posible position
        self.leave = False          # Does a word end here

    # Recursive append tree parts
    def append(self, item):
        if len(item) > 0:
            index = ord(item[0]) - ord('a')
            if index < 0 or index > 26: return
            if self.children[index] == None:
                newNode = Tree()
                self.children[index] = newNode
            if len(item) == 1:
                self.children[index].leave = True
            self.children[index].append(item[1:])

    # Contains with index te prevent string copies
    def contains(self, item, item_index):
        if self.has_node(item[item_index]):
            if len(item) == item_index +1:
                return self.get_child(item[item_index]).leave
            return self.get_child(item[item_index]).contains(item, item_index + 1)
    
    # For pythons in syntax
    def __contains__(self, item):
        return self.contains(item, 0)

    def get_child(self, char):
        index = ord(char) - ord('a')
        return self.children[index]

    def has_node(self, char):
        return self.get_child(char) != None




class Board():
    def __init__(self, N, tree):
        self.N = N
        self.tree = tree
        self.cels = [N*[0] for _ in range(N)]
        for x in range(N):
            for y in range(N):
                self.cels[y][x] = chr(97+random.randint(0, 26-1)) # random is inclusive

    # print board
    def __str__(self):
        string = "__Board__\n"
        for b in self.cels:
            string += str(b) + "\n"
        return string

    def search_generator(self, y,x, subtree, prefix="", history=[]):
        connection = history + [self.N*y + x]
        if len(set(connection)) == len(connection): # in Boggle you can not use a position twice
            if subtree.has_node(self.cels[y][x]):  # if there are still words left in the word list
                childtree = subtree.get_child(self.cels[y][x])
                if childtree.leave:
                    yield prefix + self.cels[y][x]

                yield from self.search_generator((self.N + y+1) % self.N, (self.N + x  ) % self.N, childtree, prefix + self.cels[y][x], connection)
                yield from self.search_generator((self.N + y  ) % self.N, (self.N + x+1) % self.N, childtree, prefix + self.cels[y][x], connection)
                yield from self.search_generator((self.N + y-1) % self.N, (self.N + x  ) % self.N, childtree, prefix + self.cels[y][x], connection)
                yield from self.search_generator((self.N + y  ) % self.N, (self.N + x-1) % self.N, childtree, prefix + self.cels[y][x], connection)
    

    def search_all_generator(self):
        for y in range(self.N):
            for x in range(self.N):
                yield from self.search_generator(y,x, self.tree) # yield from is a strange python syntax to pass on the result of a generator because the default is to yield the generator object itself




n = int(input("Board size: "))
searchTree = Tree()
board = Board(n, searchTree)

with open("words.txt","r") as f:  # the file provided by the hanze is not utf-8 so we removed the last entrie
    for line in f:
        for word in line.split("\n"):
            searchTree.append(word.lower())
assert("tab" in searchTree)


print(board)
for item in board.search_all_generator():
    print(item)
