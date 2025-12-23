import sys
import os

# Add the parent directory to sys.path to resolve 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.vibes import get_raw
dash = "-" * 20

url_text = get_raw(day=3, year=2015)
url_text = url_text.strip()
# url_text = url_text[:10]

location = [0, 0]
locs = [0, 0]

"""
for idx, ch in enumerate(url_text):
    if ch == '^':
        location[1] += 1
    elif ch == 'v':
        location[1] -= 1
    elif ch == '<':
        location[0] -= 1
    elif ch == '>':
        location[0] += 1
    locs.append(location.copy())
    # print(f"[{idx:03}] {location}")

unique = set(tuple(x) for x in locs)
num_unique = len(unique)
"""


deltas = {
    '^': ( 0,  1),
    'v': ( 0, -1),
    '<': (-1,  0),
    '>': ( 1,  0),
}

for ch in url_text:
    dx, dy = deltas.get(ch, (0, 0))  # Unknown chars do nothing
    location = (location[0] + dx, location[1] + dy)
    locs.append(location)

unique = set(locs)
num_unique = len(unique)

print(dash)
print(f"num_unique (part 1):{num_unique}")

def walk_path(text: str) -> set[tuple[int, int]]:
    """Return the set of visited coordinates starting at (0,0) for a single walker."""
    x, y = 0, 0
    visited = {(0, 0)}
    for ch in text:
        dx, dy = deltas.get(ch, (0, 0))  # ignore unknown chars
        x += dx
        y += dy
        visited.add((x, y))
    return visited

# Split instructions between Santa (even indices) and Robo-Santa (odd indices)
santa_text = url_text[0::2]
robo_text  = url_text[1::2]

santa_visited = walk_path(santa_text)
robo_visited  = walk_path(robo_text)

# Union of visited houses (starting house is included in both)
total_visited = santa_visited | robo_visited
num_unique = len(total_visited)

print(dash)
print(f"odd_num_unique (Santa): {len(santa_visited)}")
print(f"even_num_unique (Robo): {len(robo_visited)}")
print(f"total_num_unique (union): {num_unique}")
print(dash)
