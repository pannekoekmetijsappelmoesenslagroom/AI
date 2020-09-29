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
#print(a)
#print()

def transpose(rows):
    return [list(i) for i in zip(*rows)]

cols = transpose(rows)

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


# TODO: kan nog versnelt worden door ..._has_1_at te gebruiken
def cover(r, row_valid, col_valid):
    # given the selected row r set related cols and rows invalid
    # appr. 75% of the time is spent in this function
    for x, current_col_valid in enumerate(col_valid):
        if current_col_valid:
            if r[x] == True:
                for y, current_row_valid in enumerate(row_valid):
                    if current_row_valid:
                        if a[y][x] == 1:
                            row_valid[y] = 0

    return row_valid


# kan nog versneld worden door best kolom terug te geven met minste 1'en
def select_col(col_valid):
    for i,v in enumerate(col_valid):
        if v == 1:
            return i 


def solve(row_valid, col_valid, partial_solution):
    if not any(col_valid): 
        print("exact cover has been found", partial_solution)
        yield partial_solution

    if any(row_valid): # Als er nog een rij bij de potentiele oplossing te stoppen is gaan we door
        selected_col_index = select_col(col_valid) # Selecteer een kolom (met minste 1'en om sneller te zijn)
        for r_index in col_has_1_at[selected_col_index]:    # voor iedere rij met een gemeenschappelijke 1 met de geselecteerde kolom
            row_valid_copy = row_valid.copy(); col_valid_copy = col_valid.copy() # onthoud oude situatie
            
            row_valid = cover(a[r_index], row_valid, col_valid) # cover de rijen die niks meer gaan toevoegen
            for i,v in enumerate(a[r_index]): # update nu welke kolommen nog niet gevult zijn
                if v == True:
                    col_valid[i] = 0    
            yield from solve(row_valid, col_valid, partial_solution + [r_index]) # DFS

            row_valid = row_valid_copy; col_valid = col_valid_copy  # het vorige pad heeft niks opgelefert dus we gaan terug naar de vorige situatie


# all_solutions = list(solve(row_valid, col_valid, []))

for solution in solve(row_valid, col_valid, []):
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
