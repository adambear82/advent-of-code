# -------- boilerplate -------- 

import sys, os#, itertools
from tabulate import tabulate # sudo apt install python3-tabulate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe, dash, dec_print, prints

# --------- definitions ---------



# -------- main -----------------

wipe()
part(8)

triangles = get_raw(day=3, year=2016, file_name="input.txt")
triangles = triangles.strip().split("\n")
triangles = [i.split() for i in triangles]
print(triangles[:4], "...")

part(9)
tri_sum = int(triangles[0][0]) + int(triangles[0][1])
boo = tri_sum > int(triangles[0][2])
print(f"{triangles[0][0]} + {triangles[0][1]} = {tri_sum} > {triangles[0][2]}, {boo} triangle")


part(1)

counter = 0
for a, b, c in triangles :
    a = int(a)
    b = int(b)
    c = int(c)
    if a + b > c and a + c > b and b + c > a :
        counter += 1
print(f"true triangles: {counter}")

part(2)


def is_triangle(a, b, c):
    a = int(a)
    b = int(b)
    c = int(c)
    return a + b > c and a + c > b and b + c > a

counter = 0

# Process input in chunks of 3 rows
for i in range(0, len(triangles), 3):
    block = triangles[i:i+3]         # take 3 rows
    cols = zip(*block)               # transpose (column-wise)

    # Each column produces one triangle
    for a, b, c in cols:
        if is_triangle(a, b, c):
            counter += 1

print("Column-wise true triangles:", counter)

