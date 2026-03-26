# -------- boilerplate -------- 

import sys, os#, itertools
# from tabulate import tabulate # sudo apt install python3-tabulate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe# dash, dec_print, prints

# --------- definitions ---------

def is_triangle(a, b, c):
    return a + b > c and a + c > b and b + c > a

# -------- main -----------------

wipe()
part(8)

triangles = get_raw(day=3, year=2016, file_name="input.txt")
triangles = triangles.strip().split("\n")
triangles = [i.split() for i in triangles]
triangles = [[int(j) for j in i] for i in triangles]
print(triangles[:4], "...")

part(9)

tri_sum_0 = triangles[0][0] + triangles[0][1]
tri_sum_3 = triangles[3][2] + triangles[3][1]
boo_0 = tri_sum_0 > triangles[0][2]
boo_3 = tri_sum_3 > triangles[3][0]
print(f"{triangles[0][0]} + {triangles[0][1]} = {tri_sum_0} > {triangles[0][2]}, {boo_0} triangle")
print(f"{triangles[3][2]} + {triangles[3][1]} = {tri_sum_3} > {triangles[3][0]}, {boo_3} triangle")

part(1)

counter = 0
for a, b, c in triangles :
    if is_triangle(a, b, c) :
        counter += 1
print(f"true triangles: {counter}")

part(2)
counter = 0

# Process input in chunks of 3 rows
for i in range(0, len(triangles), 3):
    block = triangles[i:i+3]         # take 3 rows
    cols = zip(*block)               # transpose (column-wise)

    # Each column produces one triangle
    for a, b, c in cols:
        if is_triangle(a, b, c):
            counter += 1

print(f"Column-wise true triangles: {counter}\n")

