from utils.vibes import get_raw  # type: ignore
import re # import regular expressions
from collections import defaultdict

url_text = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

url_text = get_raw(12)

# Split into blocks
blocks = url_text.strip().split("\n\n") # split into blocks
patterns_block = "\n\n".join(blocks[:6]) # join everything up to 6 blocks
metrics_block = "\n\n".join(blocks[6:]) # join everything after 6 blocks

print(f"\npatterns_block:\n\n{patterns_block}\n")
# print(f"\nmetrics_block:\n\n{metrics_block}\n")

pattern, patterns = [], []
for block in patterns_block.split("\n\n"): # split patterns_block into block
    for line in block.split("\n"): # split block into lines
        pattern.append(line)
    patterns.append(pattern[1:]) # chop the 0 label
    pattern = [] # reset pattern to empty list

metrics_str = []
for line in metrics_block.split("\n"): # split metrics_block into line
    metrics_str.append(line)

# print(f"\nmetrics_str:\n\n{metrics_str}\n")

metrics = []
for item in metrics_str:
    nums = list(map(int, re.findall(r'\d+', item))) # find all numbers in item
    metrics.append(nums)


print(f"\npatterns:\n\n{patterns}\n")
print(f"\nmetrics:\n\n{metrics}\n")



def transform(strings, mode='horizontal'):
    """
    Transform a list of equal-length strings as a 2D grid.

    Modes:
      - 'horizontal' : flip each row left↔right
      - 'vertical'   : flip rows top↔bottom
      - 'both'       : flip horizontally and vertically (same as rotate180)
      - 'rotate90'   : rotate 90° clockwise
      - 'rotate180'  : rotate 180°
      - 'rotate270'  : rotate 270° clockwise (or 90° counter-clockwise)

    Args:
        strings (list[str]): e.g., ['abc', 'def', 'ghi']
        mode (str): one of the modes above

    Returns:
        list[str]: transformed list of strings

    Notes:
        - Assumes all strings have the same length (rectangular grid).
        - Raises ValueError for unknown modes or empty input.
    """
    if not strings:
        return []

    # Validate rectangular shape (optional but helpful)
    width = len(strings[0])
    if any(len(row) != width for row in strings):
        raise ValueError("All strings must have the same length (rectangular grid).")

    if mode == 'horizontal':
        # Reverse each row
        return [row[::-1] for row in strings]

    elif mode == 'vertical':
        # Reverse the order of rows
        return strings[::-1]

    elif mode == 'both':
        # Reverse rows and each row's content (equivalent to rotate180)
        return [row[::-1] for row in strings[::-1]]

    elif mode == 'rotate90':
        # Transpose (using zip) then reverse rows → 90° clockwise
        # Example: ['abc','def','ghi'] -> ['gda','heb','ifc']
        cols = zip(*strings[::-1])  # reverse rows, then transpose
        return [''.join(col) for col in cols]

    elif mode == 'rotate180':
        # Same as both flips
        return [row[::-1] for row in strings[::-1]]

    elif mode == 'rotate270':
        # Transpose then reverse columns → 270° clockwise (90° CCW)
        cols = zip(*strings)
        rotated = [''.join(col) for col in cols][::-1]
        return rotated

    else:
        raise ValueError("mode must be one of: 'horizontal', 'vertical', 'both', "
                         "'rotate90', 'rotate180', 'rotate270'")


# print("\nnormal\n" + "\n".join(patterns[0]))
# print("\nhorizontal\n" + "\n".join(transform(patterns[0], 'horizontal')))
# print("\nvertical\n" + "\n".join(transform(patterns[0], 'vertical')))
# print("\nboth\n" + "\n".join(transform(patterns[0], 'both')))
# print("\nrotate90\n" + "\n".join(transform(patterns[0], 'rotate90')))
# print("\nrotate180\n" + "\n".join(transform(patterns[0], 'rotate180')))
# print("\nrotate270\n" + "\n".join(transform(patterns[0], 'rotate270')))

# transposing metrics is slow
"""
matrices = zip(*metrics)
matrices = list(matrices)
matrices = matrices[:2]
matrices = zip(*matrices)
matrices = list(matrices)
"""

# matrices and commands were not required in co pilot code
"""
matrices = [tuple(row[:2]) for row in metrics] # only take the first two columns
commands = [tuple(row[2:]) for row in metrics] # only take after the first two columns
print(f"\nmatrices:\n\n{matrices}\n")
print(f"\ncommands:\n\n{commands}\n")
"""

# co pilot generated code
# ------------------------------
# Shape normalization & variants
# ------------------------------
def grid_to_coords(grid):
    """Return normalized tuple of (r, c) coords of '#' cells."""
    coords = [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == '#']
    if not coords:
        return tuple()
    min_r = min(r for r, _ in coords)
    min_c = min(c for _, c in coords)
    norm = sorted([(r - min_r, c - min_c) for r, c in coords])
    return tuple(norm)

# all unique transforms we’ll generate
sym_ops = ['horizontal', 'vertical', 'both', 'rotate90', 'rotate180', 'rotate270']

shape_variants = []  # list of variants per shape
shape_areas = []
for shp in patterns:
    variants = {grid_to_coords(shp)}  # identity
    for m in sym_ops:
        t = transform(shp, m)
        variants.add(grid_to_coords(t))
    vlist = sorted([v for v in variants if v], key=lambda x: (len(x), x))
    shape_variants.append(vlist)
    shape_areas.append(len(vlist[0]))  # area is constant across variants

# ------------------------------
# Build regions and required counts
# ------------------------------
regions = []
for row in metrics:
    W, H = row[0], row[1]
    counts = row[2:]
    regions.append((W, H, counts))

# ------------------------------
# Precompute placements for a region
# ------------------------------
def placements_for_region(W, H):
    """Return:
    - placements_by_shape: list[shape_id -> list[int bitmask]],
    - placements_by_cell: dict[cell_index -> list[(shape_id, bitmask)]].
    """
    placements_by_shape = []
    placements_by_cell = defaultdict(list)

    def cell_index(r, c):
        return r * W + c

    for sid, variants in enumerate(shape_variants):
        sid_placements = []
        for coords in variants:
            max_r = max(r for r, _ in coords)
            max_c = max(c for _, c in coords)
            # slide bounding box
            for base_r in range(H - max_r):
                for base_c in range(W - max_c):
                    bit = 0
                    for (dr, dc) in coords:
                        r = base_r + dr
                        c = base_c + dc
                        bit |= 1 << cell_index(r, c)
                    sid_placements.append(bit)
        # uniqueness across orientations
        sid_placements = list(set(sid_placements))
        placements_by_shape.append(sid_placements)
        for bit in sid_placements:
            b = bit
            while b:
                lsb = b & -b
                idx = (lsb.bit_length() - 1)
                placements_by_cell[idx].append((sid, bit))
                b ^= lsb

    return placements_by_shape, placements_by_cell

# ------------------------------
# DFS exact cover with counts (allow empty cells)
# ------------------------------
def can_fit(W, H, counts, want_solution=False):
    total_cells = W * H
    required_area = sum(shape_areas[i] * counts[i] for i in range(len(counts)))
    # Presents must fit but don't need to fill the grid
    if required_area > total_cells:
        return False, None

    placements_by_shape, placements_by_cell = placements_for_region(W, H)

    occ = 0
    remaining_counts = counts[:]
    solution = []

    # Quick feasibility: if a required shape has no placements at all
    shape_has_placements = [bool(placements_by_shape[i]) for i in range(len(remaining_counts))]
    for i, cnt in enumerate(remaining_counts):
        if cnt > 0 and not shape_has_placements[i]:
            return False, None

    def all_placed():
        return sum(remaining_counts) == 0

    def choose_next_cell():
        """Pick an uncovered cell that has at least one candidate placement given remaining shapes.
        Use min-branching heuristic."""
        best_idx = None
        best_cands = None
        best_len = 10**9
        for idx in range(total_cells):
            if (occ >> idx) & 1:
                continue
            cands = [p for (sid, p) in placements_by_cell[idx]
                     if remaining_counts[sid] > 0 and (p & occ) == 0]
            if cands and len(cands) < best_len:
                best_len = len(cands)
                best_idx = idx
                best_cands = cands
        return best_idx, best_cands

    def dfs():
        nonlocal occ
        if all_placed():
            return True
        idx, cands = choose_next_cell()
        if idx is None:
            # No cell left with candidates, but still shapes to place
            return False
        for p in sorted(cands, key=lambda x: -x.bit_count()):
            sids = [sid for (sid, bit) in placements_by_cell[idx] if bit == p]
            for sid in sids:
                if remaining_counts[sid] <= 0 or (p & occ) != 0:
                    continue
                remaining_counts[sid] -= 1
                occ ^= p
                solution.append((sid, p))
                if dfs():
                    return True
                solution.pop()
                occ ^= p
                remaining_counts[sid] += 1
        return False

    solved = dfs()
    if not solved:
        return False, None

    if not want_solution:
        return True, None

    # Build visualization
    grid = [['.' for _ in range(W)] for _ in range(H)]
    letters = [chr(ord('A') + i) for i in range(len(shape_variants))]
    def write_bit(letter, bit):
        b = bit
        while b:
            lsb = b & -b
            idx = (lsb.bit_length() - 1)
            r, c = divmod(idx, W)
            grid[r][c] = letter
            b ^= lsb
    for sid, bit in solution:
        write_bit(letters[sid], bit)
    vis = '\n'.join(''.join(row) for row in grid)
    return True, vis

# ------------------------------
# Run all regions
# ------------------------------
results = []
solutions = []
for (W, H, counts) in regions:
    ok, vis = can_fit(W, H, counts, want_solution=True)
    results.append(ok)
    solutions.append((W, H, counts, vis))

num_fit = sum(1 for x in results if x)

for item in solutions:
    print(item[0], 'x', item[1], item[2])
    print(item[3] if item[3] else 'NO SOLUTION')
    print('-'*20)

print(num_fit)
