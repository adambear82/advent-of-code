import sys
import os

# Add the parent directory to sys.path to resolve 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.vibes import get_raw

url_text = get_raw(day=2, year=2015)
url_text = url_text.strip().splitlines()

str_dim = [line.split('x') for line in url_text]
int_dim = [[int(x) for x in line] for line in str_dim]
labels = ["l", "w", "h"]

total_area = 0
for idx, dims in enumerate(int_dim, start=0): # idx is the index of the current dimension
    d = dict(zip(labels, dims)) # d is a dictionary of the current cuboid's dimensions
    LW = d["l"] * d["w"] # LW is the area of the current cuboid's length and width
    HW = d["h"] * d["w"] # HW is the area of the current cuboid's height and width
    HL = d["h"] * d["l"] # HL is the area of the current cuboid's height and length
    m = min(LW, HW, HL) # m is the smallest of the three areas
    area = 2 * (LW + HW + HL) + m # area is the total area of the current cuboid
    total_area += area # total_area is the total area of all cuboids
    dims_display = "[" + ", ".join(f"{x:02}" for x in dims) + "]" # dims_display is the string representation of the current cuboid's dimensions
    print(f"{idx:03}: {dims_display} area = {area:04},  total = {total_area}") # print the current cuboid's dimensions and area
