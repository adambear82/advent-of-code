import sys, os, platform
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part

import re
from typing import List, Tuple

# --------------------------------------------------------------

def create_grid(width_height = 10):
    return [[0 for _ in range(width_height)] for _ in range(width_height)]

def display_grid(grid, style="preview"):
    
    if style == "list":
        # to print the grid with commas between the numbers
        for row in grid:
            print(row)
    
    elif style == "preview":
        # to print the grid with spaces between the numbers
        preview = "\n".join([" ".join(map(str, row)) for row in grid])
        print(preview)

    else:
        print("Invalid style") 
    
    print()

def fill_rectangle(grid, x1, y1, x2, y2, value=1):
    """
    Set all cells in the rectangle defined by (x1, y1) through (x2, y2) to `value`.
    Coordinates are inclusive. Works regardless of the order of the corners.
    """
    # Normalize coordinates so (x1, y1) is top-left and (x2, y2) is bottom-right
    left, right = sorted((x1, x2))
    top, bottom = sorted((y1, y2))

    # Clamp to grid bounds (optional safety, assuming 0 <= x,y < 1000)
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1
    left = max(0, min(left, max_x))
    right = max(0, min(right, max_x))
    top = max(0, min(top, max_y))
    bottom = max(0, min(bottom, max_y))

    # Fill the rectangle
    for y in range(top, bottom + 1):
        row = grid[y]
        for x in range(left, right + 1):
            row[x] = value

def toggle_rectangle(grid, x1, y1, x2, y2):
    left, right = sorted((x1, x2))
    top, bottom = sorted((y1, y2))
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1
    left = max(0, min(left, max_x))
    right = max(0, min(right, max_x))
    top = max(0, min(top, max_y))
    bottom = max(0, min(bottom, max_y))
    for y in range(top, bottom + 1):
        row = grid[y]
        for x in range(left, right + 1):
            row[x] = 1 - row[x]  # invert

def extract(text: str) -> List[Tuple[int, int]]:
    """
    Extracts two (x, y) coordinate pairs from strings that use 'through' as the separator.
    Examples:
        "887,9 through 959,629"
        "  887 , 9   THROUGH   959 , 629  "  (case-insensitive, flexible spacing)
    Returns:
        [(x1, y1), (x2, y2)] or [] if no match.
    """
    pattern = re.compile(
        r'\s*(\d+)\s*,\s*(\d+)\s*through\s*(\d+)\s*,\s*(\d+)\s*',
        re.IGNORECASE
    )
    m = pattern.search(text)
    if not m:
        return []
    x1, y1, x2, y2 = map(int, m.groups())
    return [(x1, y1), (x2, y2)]

def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def sum_grid(grid):
    return sum(cell for row in grid for cell in row)

def wipe():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def increase_rectangle(grid, x1, y1, x2, y2, value=1):
    """
    Set all cells in the rectangle defined by (x1, y1) through (x2, y2) to `value`.
    Coordinates are inclusive. Works regardless of the order of the corners.
    """
    # Normalize coordinates so (x1, y1) is top-left and (x2, y2) is bottom-right
    left, right = sorted((x1, x2))
    top, bottom = sorted((y1, y2))

    # Clamp to grid bounds (optional safety, assuming 0 <= x,y < 1000)
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1
    left = max(0, min(left, max_x))
    right = max(0, min(right, max_x))
    top = max(0, min(top, max_y))
    bottom = max(0, min(bottom, max_y))

    # Fill the rectangle
    for y in range(top, bottom + 1):
        row = grid[y]
        for x in range(left, right + 1):

            # if the value is less than 0, set it to 0
            # otherwise, add the value to the cell
            if row[x] + value >= 0: 
                row[x] += value
            else:
                row[x] = 0

# --------------------------------------------------------------

wipe()
part(1)

print("create an example grid\n")
grid = create_grid()
display_grid(grid)

print("adjust single value in example grid\n")
grid[0][0] = 1
display_grid(grid)

print("fill rectangle in example grid\n")
fill_rectangle(grid, 0, 0, 5, 5)
display_grid(grid)

print("count the number of 1s in the grid:")
print(sum_grid(grid))

print("\npreview first 10 instructions from the input\n")
input_txt = get_raw(day=6, year=2015)
input_txt = input_txt.strip().splitlines()
input_preview = input_txt[:10]
input_joined = "\n".join(input_preview)
print(input_joined, "\n")

print("create a new blank 1000x1000 grid\n")
grid = create_grid(1000)

# parse the input for part 1
rows_part_1 = []
print("parse the input\n")
for row in input_txt:
    line = []

    if row[0:7] == "turn on":

        line.append("turn on")
        c = extract(row[8:])
        line.append(c)

        fill_rectangle(grid, c[0][0], c[0][1], c[1][0], c[1][1], value=1)

    elif row[0:8] == "turn off":
        line.append("turn off")
        c = extract(row[9:])
        line.append(c)

        fill_rectangle(grid, c[0][0], c[0][1], c[1][0], c[1][1], value=0)

    elif row[0:6] == "toggle":
        line.append("toggle")
        c = extract(row[7:])
        line.append(c)

        toggle_rectangle(grid, c[0][0], c[0][1], c[1][0], c[1][1])

    else:
        line.append("error")

    line = flatten(line)
    rows_part_1.append(line)

print("\n".join(map(str, rows_part_1[:10])))

print("\npreview the grid\n")

segment = [row[750:760] for row in grid[750:760]]
preview = "\n".join([" ".join(map(str, row)) for row in segment])
print(preview)

# print("\ndisplay the whole grid\n")
# display_grid(grid)

print("\ncount the number of 1s in the grid for part 1:")
print(sum_grid(grid))

part(2)

print("create a new blank 1000x1000 grid\n")
grid_part_2 = create_grid(1000)

# parse the input for part 2
rows_part_2 = []
print("parse the input\n")
for row in input_txt:
    line = []

    if row[0:7] == "turn on":

        line.append("increase by 1")
        c = extract(row[8:])
        line.append(c)

        increase_rectangle(grid_part_2, c[0][0], c[0][1], c[1][0], c[1][1], value=1)

    elif row[0:8] == "turn off":
        line.append("decrease by 1")
        c = extract(row[9:])
        line.append(c)

        increase_rectangle(grid_part_2, c[0][0], c[0][1], c[1][0], c[1][1], value=-1)

    elif row[0:6] == "toggle":
        line.append("increase by 2")
        c = extract(row[7:])
        line.append(c)

        increase_rectangle(grid_part_2, c[0][0], c[0][1], c[1][0], c[1][1], value=2)

    else:
        line.append("error")

    line = flatten(line)
    rows_part_2.append(line)

print("\n".join(map(str, rows_part_2[:10])))

print("\npreview the grid\n")

segment = [row[750:760] for row in grid_part_2[750:760]]
preview = "\n".join([" ".join(map(str, row)) for row in segment])
print(preview)

# print("\ndisplay the whole grid\n")
# display_grid(grid_part_2)

print("\ncount the level of illumination in the grid for part 2:")
print(sum_grid(grid_part_2))
