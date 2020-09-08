"""
Vraag: wat is de tijdcomplexiteit van je oplossing?

n = board size
hinst lijst maken: n*n * log(n)
board find 1: n*n
vullen: 4*n*n* n*n/len(hints)

O(n^4)
"""

class Board():
    def __init__(self, N):
        self.N = N
        self.cels = [N*[0] for _ in range(N)]
        self.hints = [0]

    # print board
    def __str__(self):
        string = "__Board__\n"
        for b in self.cels:
            for i in b:
                string += str(i) + "\t"
            string += "\n"
        return string

    # valid manhaten neighbours 
    def __neighbours(self, y,x): # todo
        if y+1 <= self.N-1:  yield (y+1,x)
        if x+1 <= self.N-1:  yield (y,x+1)
        if y-1 >= 0:         yield (y-1,x)
        if x-1 >= 0:         yield (y,x-1)
    
    # Depth first recursive solving generator
    def __solve(self, y,x, stepcount, hints_index):
        if stepcount <= self.hints[hints_index]: # looking higher than the hint has no purpose
            if stepcount == self.hints[hints_index] and self.cels[y][x] == stepcount:
                hints_index += 1
                if stepcount == self.N**2: # if at last hint
                    yield self.__str__()
                    return

            if self.cels[y][x] == 0 or self.cels[y][x] == stepcount:
                do_reset = self.cels[y][x] == 0
                self.cels[y][x] = stepcount
                for ny,nx in self.__neighbours(y,x):
                    yield from self.__solve(ny,nx, stepcount+1, hints_index)
                if do_reset:
                    self.cels[y][x] = 0

    def solutions_generator(self):
        tmp = set()
        for array in self.cels:
            for x in array:
                tmp.add(x)
        self.hints = sorted(list(tmp))
        index = 1     # 0 and 1 are the first 2 so we skip those

        for y in range(self.N):
            for x in range(self.N):
                if self.cels[y][x] == 1: # 3 line version of np.where(1)
                    yield from self.__solve(y, x, 1, index)


# board = Board(3)  # this one has 2 solution
# board.cels = [
#     [1, 0, 0],
#     [0, 5, 0],
#     [0, 0, 9],
# ]

board = Board(9)
board.cels = [
    [0, 0, 0, 0, 0, 0, 0, 0, 81],
    [0, 0, 46, 45, 0, 55, 74, 0, 0],
    [0, 38, 0, 0, 43, 0, 0, 78, 0],
    [0, 35, 0, 0, 0, 0, 0, 71, 0],
    [0, 0, 33, 0, 0, 0, 59, 0, 0],
    [0, 17, 0, 0, 0, 0, 0, 67, 0],
    [0, 18, 0, 0, 11, 0, 0, 64, 0],
    [0, 0, 24, 21, 0, 1, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

for solution in board.solutions_generator():
    print(solution)