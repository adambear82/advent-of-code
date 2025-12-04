# Advent of Code 2025 - Day 04
import requests

#  Get input data from GitHub, couldn't use Advent of Code site directly
url = "https://raw.githubusercontent.com/adambear82/advent-of-code/refs/heads/main/2025/day-04/input.txt"
resp = requests.get(url, timeout=10)
url_text = resp.text.strip().splitlines()

# For debugging, here's a sample input list
url_dbug = [
            # (.) = empty space, (@) = roll, (x) = accessible roll    
            # initial values, 1st pass 13 x --->    final pass 43 x

            "..@@.@@@@.",    # ..xx.xx@x.   --->    ..xx.xxxx.
            "@@@.@.@.@@",    # x@@.@.@.@@   --->    xxx.x.x.xx
            "@@@@@.@.@@",    # @@@@@.x.@@   --->    xxxxx.x.xx
            "@.@@@@..@.",    # @.@@@@..@.   --->    x.xx@@..x.
            "@@.@@@@.@@",    # x@.@@@@.@x   --->    xx.@@@@.xx
            ".@@@@@@@.@",    # .@@@@@@@.@   --->    .xx@@@@@.x
            ".@.@.@.@@@",    # .@.@.@.@@@   --->    .x.@.@.@@x
            "@.@@@.@@@@",    # x.@@@.@@@@   --->    x.x@@.@@@x
            ".@@@@@@@@.",    # .@@@@@@@@.   --->    .xx@@@@@x.
            "@.@.@@@.@."     # .@@@@@@@@.   --->    x.x.@@@.x.
            ]


# Relative positions of the 8 neighbouring cells
neighbours = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
]

# check if (row, col) is within the grid bounds
def in_bounds(grid, row, col):
    return (
        0 <= row < len(grid) and
        0 <= col < len(grid[row])
    )

# count the number of adjacent rolls ('@') around the cell at (row, col)
def count_adjacent_rolls(grid, row, col):
    count = 0

    # neighbours is a list of (delta_row, delta_col)
    for delta_row, delta_col in neighbours:
        neighbour_row = row + delta_row
        neighbour_col = col + delta_col
        
        # Check if the neighbour is within bounds and is a roll ('@')
        if (
            in_bounds(grid, neighbour_row, neighbour_col) and
            grid[neighbour_row][neighbour_col] == '@'
        ):
            count += 1
    return count

# if the roll at (row, col) is accessible, count adjacent rolls < 4
def is_accessible(grid, row, col):
    if grid[row][col] != '@':
        return False
    return count_adjacent_rolls(grid, row, col) < 4

# mark accessible rolls with 'x'
def mark_accessible(grid):
    height = len(grid)
    width = len(grid[0])

    # mutable copy as list of lists of chars
    out = [list(row) for row in grid]

    for r in range(height):
        for c in range(width):
            if is_accessible(grid, r, c):
                out[r][c] = 'x'

    # Convert back to strings 
    return [''.join(row) for row in out]

# part 1 - mark accessible rolls and count them
marked = mark_accessible(url_text)
count_x = sum(row.count('x') for row in marked)


# part 2 - repeatedly remove accessible rolls until stable
def remove_until_stable(grid):

    # grid[:] creates a shallow copy: new outer list, same inner elements
    current = grid[:]

    # loop until false detected meaning no more changes
    while True:
        # compute next by marking accessible rolls
        nxt = mark_accessible(current)
        # when the next iteration is the same as the current, return it
        if nxt == current:
            return nxt
        # otherwise continue with next as current
        current = nxt

final_grid = remove_until_stable(url_text)
total_removed = sum(row.count('x') for row in final_grid)

# print with type
final_output = (total_removed)
print(final_output, type(final_output))
