from utils.vibes import get_raw  # type: ignore

# Utilities created with copilot step by step by me

def normalize_rows(rows):
    """Strip trailing spaces and assert equal widths."""
    cleaned = [r.rstrip() for r in rows]
    w = len(cleaned[0])
    assert all(len(r) == w for r in cleaned), "All rows must have equal length"
    return cleaned

def replace_in_rows(rows, row_idx, col_idx, new_char="|"):
    """Replace the character at (row_idx, col_idx) and return a NEW rows list."""
    line = rows[row_idx]
    updated_line = line[:col_idx] + new_char + line[col_idx+1:]
    new_rows = rows.copy()
    new_rows[row_idx] = updated_line
    return new_rows

def find_laser_start(rows):
    """Return (row, col) for 'S'."""
    for i, line in enumerate(rows):
        j = line.find('S')
        if j != -1:
            return (i, j)
    raise ValueError("No 'S' found")


def move_down(pos):
    """Move position one row down."""
    r, c = pos
    return (r + 1, c)


def laser_hits_splitter(rows):
    """
    For every column, if a splitter '^' has a laser '|' directly above it,
    mark that splitter as 'X'. Returns a NEW rows list.
    """
    rows = normalize_rows(rows)
    cols = [list(col) for col in zip(*rows)]  # cols[c][r] => char at (r, c)
    height = len(rows)
    width = len(rows[0])

    for c in range(width):
        for r in range(1, height):
            if cols[c][r] == '^' and cols[c][r-1] == '|':
                cols[c][r] = 'X'  # splitter hit

    new_rows = [''.join(row_chars) for row_chars in zip(*cols)]
    return new_rows


def mark_adjacent_dots(rows):
    """
    For each row, replace '.' immediately left/right of 'X' with '|'.
    i.e., '.X' -> '|X' and 'X.' -> 'X|'.
    Returns a NEW list of rows.
    """
    rows = normalize_rows(rows)
    new_rows = []
    for line in rows:
        chars = list(line)
        n = len(chars)
        for i, ch in enumerate(chars):
            if ch == 'X':
                if i - 1 >= 0 and chars[i - 1] == '.':
                    chars[i - 1] = '|'
                if i + 1 < n and chars[i + 1] == '.':
                    chars[i + 1] = '|'
        new_rows.append(''.join(chars))
    return new_rows


def laser_continues(rows):
    """
    For every column, if a space '.' has a laser '|' directly above it,
    mark that space as '|'. Returns a NEW rows list.
    """
    rows = normalize_rows(rows)
    cols = [list(col) for col in zip(*rows)]  # cols[c][r] => char at (r, c)
    height = len(rows)
    width = len(rows[0])

    for c in range(width):
        for r in range(1, height):
            if cols[c][r] == '.' and cols[c][r-1] == '|':
                cols[c][r] = '|'  # laser continues down

    new_rows = [''.join(row_chars) for row_chars in zip(*cols)]
    return new_rows


# One full cycle
def tick(rows):
    """
    Perform one cycle of the simulation:
    1) lasers continue down,
    2) splitters hit are marked X,
    3) adjacent dots around X become pipes for horizontal split.
    Returns the NEW rows.
    """
    r1 = laser_continues(rows)
    r2 = laser_hits_splitter(r1)
    r3 = mark_adjacent_dots(r2)
    return r3

""" 
# Recursive simulation until no change
def simulate_recursive(rows, max_steps=1000, step_fn=tick, _depth=0):
   
    # Recursively apply 'step_fn' (default: tick) until the grid stabilizes
    # or max_steps is reached. Returns the final rows.
    
    new_rows = step_fn(rows)
    if new_rows == rows:
        return new_rows
    if _depth >= max_steps:
        # Guard against infinite loops; return last state
        return new_rows
    return simulate_recursive(new_rows, max_steps=max_steps, step_fn=step_fn, _depth=_depth + 1)
 """

# Iterative simulation until no change (preferred in Python)
def simulate(rows, max_steps=1000, step_fn=tick, verbose=False):
    """
    Iteratively apply 'step_fn' until no change or max_steps reached.
    Returns final rows.
    """
    rows = normalize_rows(rows)
    for step in range(1, max_steps + 1):
        new_rows = step_fn(rows)
        if verbose:
            print(f"\nstep {step}\n")
            print("\n".join(new_rows))
        if new_rows == rows:
            if verbose:
                print(f"\nStabilized after {step-1} steps.")
            return new_rows
        rows = new_rows
    if verbose:
        print(f"\nReached max_steps ({max_steps}).")
    return rows

# --- Parsing the final result ---


url_text = """
.......S.......
............... 
.......^.......
............... 
......^.^......
............... 
.....^.^.^.....
............... 
....^.^...^....
............... 
...^.^...^.^...
............... 
..^...^.....^..
............... 
.^.^.^.^.^...^.
............... 
"""

url_text = get_raw(7)

# Parse and normalize rows
rows = url_text.strip().splitlines()
rows = normalize_rows(rows)

# Mark the first downward laser directly below S
start_r, start_c = find_laser_start(rows)
rows = replace_in_rows(rows, start_r + 1, start_c, '|')

# Now run the simulation until stabilized
final_rows = simulate(rows, max_steps=100, verbose=True)

print("\nFinal grid:\n")
print("\n".join(final_rows))

# Count the number of 'X' in the final grid
count_X = sum(row.count('X') for row in final_rows)
print(f"\nPart 1\nNumber of splitters hit (X): {count_X}\n")

# End of part 1

# part 2 - coded by copilot with no edits

from functools import lru_cache

def count_timelines(grid):
    """
    Count all quantum timelines through the manifold (Part Two).
    - Start just below 'S'
    - At '^' splitters: branch to (r+1, c-1) and (r+1, c+1)
    - Else: continue to (r+1, c)
    Returns the total number of timelines that reach beyond the last row.
    """
    h, w = len(grid), len(grid[0])

    # Find S
    start = None
    for r, line in enumerate(grid):
        c = line.find('S')
        if c != -1:
            start = (r, c)
            break
    if start is None:
        raise ValueError("No 'S' found in grid")

    @lru_cache(None)
    def paths(r, c):
        # Out of bounds horizontally -> dead path
        if c < 0 or c >= w:
            return 0
        # Past the bottom -> one completed timeline
        if r >= h:
            return 1
        cell = grid[r][c]
        if cell == '^':
            # Split: left and right
            return paths(r + 1, c - 1) + paths(r + 1, c + 1)
        else:
            # Continue straight down
            return paths(r + 1, c)

    sr, sc = start
    return paths(sr + 1, sc)

total = count_timelines(rows)

print(f"Part 2\nTotal quantum timelines:\n{total}")
