import sys
import itertools

def solve():
    example_input = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
    
    # If filename is provided, use it
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            input_text = f.read()
    else:
        input_text = example_input
        
    lines = input_text.strip().splitlines()
    total_presses = 0
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        parts = line.split()
        pattern_str = parts[0]
        
        # Remove brackets
        p_inner = pattern_str[1:-1]
        target = [1 if c == '#' else 0 for c in p_inner]
        num_lights = len(target)
        
        # Buttons are in the middle. Last part is joltage.
        button_parts = parts[1:-1]
        buttons = []
        for b_str in button_parts:
            # format (1,2,3) or (1)
            inner = b_str[1:-1]
            if inner:
                indices = [int(x) for x in inner.split(',')]
            else:
                indices = []
            
            # Convert to vector
            vec = [0] * num_lights
            for idx in indices:
                if 0 <= idx < num_lights:
                    vec[idx] = 1
            buttons.append(vec)
            
        min_p = gauss_min_weight(buttons, target)
        if min_p is None:
            print(f"No solution for line: {line}")
        else:
            total_presses += min_p

    print(f"Total minimum presses: {total_presses}")

def gauss_min_weight(buttons, target):
    # Matrix A: rows are lights, cols are buttons.
    rows = len(target)
    cols = len(buttons)
    
    # Create matrix.
    M = []
    for r in range(rows):
        row = [b[r] for b in buttons] + [target[r]]
        M.append(row)
        
    pivot_row = 0
    pivot_cols = []
    
    # Forward elimination
    col = 0
    while pivot_row < rows and col < cols:
        # Find pivot
        if M[pivot_row][col] == 0:
            for r in range(pivot_row + 1, rows):
                if M[r][col] == 1:
                    M[pivot_row], M[r] = M[r], M[pivot_row]
                    break
            else:
                col += 1
                continue
        
        # Eliminate below
        for r in range(pivot_row + 1, rows):
            if M[r][col] == 1:
                # XOR row
                for c in range(col, cols + 1):
                    M[r][c] ^= M[pivot_row][c]
                    
        pivot_cols.append(col)
        pivot_row += 1
        col += 1
        
    # Check consistency
    for r in range(pivot_row, rows):
        if M[r][cols] == 1:
            return None # Impossible
            
    # Back substitution to RREF
    for i in range(len(pivot_cols) - 1, -1, -1):
        p_row = i
        p_col = pivot_cols[i]
        
        # Eliminate above
        for r in range(p_row):
            if M[r][p_col] == 1:
                for c in range(p_col, cols + 1):
                    M[r][c] ^= M[p_row][c]
                    
    # Identify free columns
    pivot_set = set(pivot_cols)
    free_indices = [c for c in range(cols) if c not in pivot_set]
    num_free = len(free_indices)
    
    min_weight = float('inf')
    
    # Iterate all combinations of free variables
    for free_vals in itertools.product([0, 1], repeat=num_free):
        x = [0] * cols
        
        # Set free variables
        for i, idx in enumerate(free_indices):
            x[idx] = free_vals[i]
            
        current_weight = sum(free_vals)
        
        # Determine pivot variables
        # x_p = constant ^ sum(coeff * x_free)
        # Because in RREF, row i corresponds to pivot col pivot_cols[i]
        # and has 1 at M[i][pivot_cols[i]]
        
        valid = True
        for i, p_col in enumerate(pivot_cols):
            p_row = i
            val = M[p_row][cols] 
            
            for f_idx in free_indices:
                # If free col has 1 in this row, it contributes
                if M[p_row][f_idx] == 1:
                    val ^= x[f_idx]
            
            x[p_col] = val
            current_weight += val
            
            if current_weight >= min_weight:
                valid = False
                break
        
        if valid:
            min_weight = current_weight
            
    return min_weight

if __name__ == '__main__':
    solve()
