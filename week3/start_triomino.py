import numpy as np

# place triominoes in matrix 3 rows x 4 cols

NR_OF_COLS = 16 # 4 triominoes HB VB L RL + 12 cells
NR_OF_ROWS = 22 # 6*HB 4*VB 6*L 6*RL

triominoes = [np.array(trio) for trio in [
        # horizontal bar (HB)
        [[1,1,1]],
        # vertical bar (VB)
        [[1],[1],[1]],
        # normal L (L)
        [[1,0], [1,1]],
        # rotated L (RL)
        [[1,1], [0,1]]
    ]
]

def all_positions(T):
    # find all positions to place triomino T in matrix M (3 rows x 4 cols)
    rows, cols = T.shape
    for i in range(3+1 - rows):
        for j in range(4+1 - cols):
            M = np.zeros((3, 4), dtype='int')
            # place T in M
            M[i:i+rows, j:j+cols] = T
            yield M

# matrix rows has 22 rows x 16 cols 
# and has the following cols: HB VB L RL (0,0) (0,1) (0,2) (0,3) (1,0) .... (3,3)

rows = []
for i, P in enumerate(triominoes):
    # i points to the 4 triominoes HB VB L RL
    for A in all_positions(P):
        # add 4 zeros to each row
        A = np.append(np.zeros(4, dtype='int'), A)
        A[i] = 1
        rows.append(list(A))

a = np.array(rows)
#print(a)
#print()

# note that zip(*b) is the transpose of b
cols = [list(i) for i in zip(*rows)]

# note that when applying alg-x we're only interested in 1's
# so we add 2 lists that define where the 1's are

def find_ones(rows):
    lv_row_has_1_at = []
    for row in rows:
        x = []
        for i in range(len(row)):
            if row[i] == 1:
                x.append(i)
        lv_row_has_1_at.append(x.copy())
    return lv_row_has_1_at

row_has_1_at = find_ones(rows) # global read-only
col_has_1_at = find_ones(cols) # global read-only

for r in row_has_1_at:
    assert len(r) == 4

row_valid = NR_OF_ROWS * [1]
col_valid = NR_OF_COLS * [1]

all_solutions = []

def cover(r, row_valid, col_valid):
    # given the selected row r set related cols and rows invalid
    # appr. 75% of the time is spent in this function
    pass

def solve(row_valid, col_valid, solution):
    # using Algoritm X, find all solutions (= set of rows) given valid/uncovered rows and cols
    pass


solve(row_valid, col_valid, [])

for solution in all_solutions:
    # solutions are sorted
    # place triominoes in matrix 3 rows x 4 cols
    D = [[0 for i in range(4)] for j in range(3)]

    for row_number in solution:
        #print(row_number) # 1 6 14 21
        row_list = row_has_1_at[row_number]
        #print(row_list)   # 0 5 6 7
        idx = row_list[0]
        assert idx in [0,1,2,3]
        symbol = ['HB','VB','L ','RL'][idx]
        for c in row_list[1:]: # skip first one
            rownr = c//4-1
            colnr = c%4
            D[rownr][colnr] = symbol
    print('------------------------')

    for i in D:
        print(i)
