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
for i, triominoe in enumerate(triominoes):
    # i points to the 4 triominoes HB VB L RL
    for A in all_positions(triominoe):
        # add 4 zeros to each row
        A = np.append(np.zeros(4, dtype='int'), A)
        A[i] = 1
        rows.append(list(A))

a = np.array(rows)
# print(a)
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

def cover(chosen_row, row_valid, col_valid):
    # given the selected row r set related cols and rows invalid
    # appr. 75% of the time is spent in this function

    #5. For each column j such that A[r][j] = 1,
    #    for each row i such that A[i][j] = 1,
    #        delete row i from matrix A.
    #    delete column j from matrix A.

    did_anything = False
    for j, col in enumerate(a.T):
        #if j < 4:
        #    continue
        if rows[chosen_row][j] == 0:
            continue

        for i, row in enumerate(rows):
            #if i < 4:
            #    continue
            if row[j] == 0:
                continue
            row_valid[i] = 0

        col_valid[j] = 0
        did_anything = True

    return did_anything

    # # Cover rows (green in Jacob's presentation)
    # for i, valid in enumerate(row_valid):
    #     if valid == 0:
    #         continue
    #     r = rows[i]
    #     for j, col in enumerate(r):
    #         if j < 4:
    #             continue

    #         if a[chosen_row][j] == 1 and col == 1:
    #             row_valid[j] = 0
    #             break

    # # Cover columns (yellow-like in Jacob's presentation)
    # for i, col in enumerate(rows[chosen_row]):
    #     if i < 4:
    #         continue
    #     
    #     if col == 1:
    #         print("Cover", i)
    #         col_valid[i] = 0

def col_least_amount_of_ones(rows, col_valid):
    # Select column with least amount of one's
    colI = -1
    number_of_ones = None
    for i, col in enumerate(rows.T):
        if i < 4:
            continue
        if col_valid[i] == 0:
            continue

        c = np.count_nonzero(col == 1)
        if not number_of_ones or c < number_of_ones:
            colI = i
            number_of_ones = c
    return colI

def solve(row_valid, col_valid, solution):
    # using Algoritm X, find all solutions (= set of rows) given valid/uncovered rows and cols

    solved = True
    for i, col in enumerate(col_valid):
        if i < 4:
            continue
        if col == 1:
            solved = False
            break

    if solved:
        print("Solved:", solution)
        all_solutions.append(solution)
        return

    #print(len(row_valid), len(col_valid), solution)
    chosen_col = col_least_amount_of_ones(a, col_valid)
    print("Chosen col:", chosen_col)

    # For every row having a 1 in the chosen column
    for i, r in enumerate(rows):
        if row_valid[i] == 0:
            continue
        if r[chosen_col] == 0:
            continue
        if i in solution:
            print("Skippin")
            continue

        our_solution = solution.copy()
        our_row_valid = row_valid.copy()
        our_col_valid = col_valid.copy()

        #print("Chosen row:", i, rows[i])

        our_solution.append(i)

        did_anything = cover(i, our_row_valid, our_col_valid)
        if not did_anything:
            print("didn't do anything")
            continue

        solve(our_row_valid, our_col_valid, our_solution)

# def cover(r, row_valid, col_valid):
#     # given the selected row r set related cols and rows invalid
#     # appr. 75% of the time is spent in this function
#     pass

# def solve(row_valid, col_valid, cur_state):
#     # using Algoritm X, find all solutions (= set of rows) given valid/uncovered rows and cols
#     pass


# all_solutions = list(solve(row_valid, col_valid, []))
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

