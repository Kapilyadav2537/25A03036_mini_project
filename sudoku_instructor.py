s = {
    11:0 , 12:0 , 13:0 ,      14:0 , 15:3 , 16:0 ,      17:9 , 18:6 , 19:0 ,
    21:0 , 22:7 , 23:0 ,      24:9 , 25:0 , 26:1 ,      27:0 , 28:3 , 29:0 ,
    31:0 , 32:0 , 33:0 ,      34:0 , 35:0 , 36:0 ,      37:0 , 38:0 , 39:1 ,

    41:0 , 42:2 , 43:5 ,      44:0 , 45:6 , 46:0 ,      47:3 , 48:0 , 49:7 ,
    51:0 , 52:6 , 53:0 ,      54:2 , 55:0 , 56:3 ,      57:0 , 58:1 , 59:0 ,
    61:4 , 62:0 , 63:3 ,      64:0 , 65:9 , 66:0 ,      67:6 , 68:8 , 69:0 ,

    71:3 , 72:0 , 73:0 ,      74:0 , 75:0 , 76:0 ,      77:0 , 78:0 , 79:0 ,
    81:0 , 82:8 , 83:0 ,      84:3 , 85:0 , 86:6 ,      87:0 , 88:2 , 89:0 ,
    91:0 , 92:4 , 93:6 ,      94:0 , 95:2 , 96:0 ,      97:0 , 98:0 , 99:0 ,
}

def print_grid(s):
    
    for r in range(1, 10):
        print(' '.join(str(s[r*10+c]) if s[r*10+c] != 0 else '.' for c in range(1, 10)))
    print()

def get_candidates_in_row(sp, row, exclude_cell=None):
    """
    Returns a list of candidate lists for all cells in the given row.
    If exclude_cell is provided, that cell is excluded from the result.
    """
    candidates = []
    for col in range(1, 10):
        cell = row * 10 + col
        if cell != exclude_cell:
            candidates += sp[cell]
    return candidates

def get_candidates_in_col(sp, col, exclude_cell=None):
    """
    Returns a list of candidate lists for all cells in the given column.
    If exclude_cell is provided, that cell is excluded from the result.
    """
    candidates = []
    for row in range(1, 10):
        cell = row * 10 + col
        if cell != exclude_cell:
            candidates += sp[cell]
    return candidates

def get_candidates_in_box(sp, sb, cell, exclude_cell=None):
    """
    Returns a list of candidate lists for all cells in the box containing 'cell'.
    If exclude_cell is provided, that cell is excluded from the result.
    """
    candidates = []
    for box_cells in sb.values():
        if cell in box_cells:
            for c in box_cells:
                if c != exclude_cell:
                    candidates += sp[c]
    return candidates

def sudoku(s):
    sp = {k: [s[k]] if s[k] != 0 else list(range(1, 10)) for k in s}
    sb = {f"b{n}": [r*10+c for r in range(R, R+3) for c in range(C, C+3)]
      for n, (R, C) in enumerate([(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)])}
    changed = True
    printed = []
    while changed:
        changed = False
        # eliminate possibilities method
        for i in s:
            if s[i] != 0:
                sp[i] = [s[i]]
            else:
                #define row and column of current cell i
                r, c = i//10, i%10

                #define set of cells in current row, column and box of current cell i
                cr = [s[r * 10 + x] for x in range(1, 10)]
                cc = [s[x * 10 + c] for x in range(1, 10)]
                cb = []
                for box in sb.values():
                    if i in box:
                        cb = [s[cell] for cell in box]
                        break
                    
                # eliminate possibilities method
                sp1 = sp[i][:]
                sp[i] = [k for k in sp[i] if k not in cc and k not in cr and k not in cb]
                if sp[i] != sp1:
                    changed = True
                if len(sp[i]) == 1 and s[i] == 0:
                    s[i] = sp[i][0]
                    print(f"Cell {i} set to {s[i]} by elimination.")
                    changed = True
        # single possible candidate among row,col,box method
        for i in s:

            r, c = i//10, i%10
            if s[i] == 0:
                for j in sp[i]:
                    if ((get_candidates_in_box(sp, sb, i, exclude_cell=i).count(j) == 0) or 
                       (get_candidates_in_row(sp, r, exclude_cell=i).count(j) == 0) or 
                       (get_candidates_in_col(sp, c, exclude_cell=i).count(j) == 0)):
                        s[i] = j
                        sp[i] = [j]
                        print(f"Cell {i} set to {s[i]} by single possible candidate.")
                        changed = True
                        break

            if len(sp[i]) == 1 and s[i] == 0:
                s[i]=sp[i][0]
                print(f"Cell {i} set to {s[i]} by single possible candidate.")
                changed = True

        for box in sb:
            for num in range(1,10):
                possible_containers = []
                for cell in sb[box]:
                    if num in sp[cell]:
                        possible_containers.append(cell)
                if 1<len(possible_containers)<4:
                    if len(possible_containers) == 2:
                        if possible_containers[0]//10 == possible_containers[1]//10:
                            r = possible_containers[1]//10
                            if [r,num,possible_containers] not in printed:
                                printed.append([r,num,possible_containers])
                                print(f"In row {r} {num} can be contained only in cells {possible_containers}")
                            for x in range(1,10):
                                if num in sp[r * 10 + x]:
                                    sp[r * 10 + x].remove(num)
                                    changed = True
                            for cell in possible_containers:
                                sp[cell].append(num)
                    elif len(possible_containers) == 2:
                        if possible_containers[0]%10 == possible_containers[1]%10:
                            c = possible_containers[1]%10
                            if [c,num,possible_containers] not in printed:
                                printed.append([c,num,possible_containers])
                            print(f"In column {c} {num} can be contained only in cells {possible_containers}")
                            for x in range(1,10):
                                if num in sp[x * 10 + c]:
                                    sp[x * 10 + c].remove(num)
                                    changed = True
                            for cell in possible_containers:
                                sp[cell].append(num)
                    elif len(possible_containers) == 3:
                        if possible_containers[0]//10 == possible_containers[1]//10 == possible_containers[2]//10:
                            r = possible_containers[1]//10
                            if [r,num,possible_containers] not in printed:
                                printed.append([r,num,possible_containers])
                            print(f"In row {r} {num} can be contained only in cells {possible_containers}")
                            for x in range(1,10):
                                if num in sp[r * 10 + x]:
                                    sp[r * 10 + x].remove(num)
                                    changed = True
                            for cell in possible_containers:
                                sp[cell].append(num)
                    elif len(possible_containers) == 3:
                        if possible_containers[0]%10 == possible_containers[1]%10 == possible_containers[2]%10:
                            c = possible_containers[1]%10
                            if [c,num,possible_containers] not in printed:
                                printed.append([c,num,possible_containers])
                            print(f"In column {c} {num} can be contained only in cells {possible_containers}")
                            for x in range(1,10):
                                if num in sp[x * 10 + c]:
                                    sp[x * 10 + c].remove(num)
                                    changed = True
                            for cell in possible_containers:
                                sp[cell].append(num)
        # pairing method
        for r in range(1,10):
            crp = [sp[r * 10 + x] for x in range(1, 10)]
            for i in crp:
                if crp.count(i) == len(i) != 1 :
                    crp.remove(i)
                    if [r,len(i),i] not in printed:
                        printed.append([r,len(i),i])
                        print(f"In row {r} {len(i)} number of cells have same possible number contents {i} which prohibits them from being contained in other cells of this row")
                    for j in crp:
                        if i != j:
                            for k in i:
                                if k in j:
                                    j.remove(k)
                                    changed = True

        for c in range(1,10):
            ccp = [sp[x * 10 + c] for x in range(1, 10)]
            for i in ccp:
                if ccp.count(i) == len(i) != 1:
                    ccp.remove(i)
                    if [c,len(i),i] not in printed:
                        printed.append([c,len(i),i])
                        print(f"In column {c} {len(i)} number of cells have same possible number contents {i} which prohibits them from being contained in other cells of this column")
                    for j in ccp:
                        if i != j:
                            for k in i:
                                if k in j:
                                    j.remove(k)
                                    changed = True

        for box in sb:
            cbp = [sp[cell] for cell in sb[box]]
            for main_container in cbp:
                if cbp.count(main_container) == len(main_container) != 1:
                    cells = [cell for cell in sb[box] if sp[cell] == main_container]
                    cbp.remove(main_container)
                    if [cells, box, main_container] not in printed:
                        printed.append([cells, box, main_container])
                        print(f"In box containing cells {cells} i.e. box {box}, only these cells can contain {main_container} which prohibits them from being contained in other cells of this box")
                    for other_container in cbp:
                        if main_container != other_container:
                            for possible_values in main_container:
                                if possible_values in other_container:
                                    other_container.remove(possible_values)
                                    changed = True

    return s

print("Initial Sudoku:")
print_grid(s)
print("Solved Sudoku:")
print_grid(sudoku(s))