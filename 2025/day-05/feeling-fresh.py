# Advent of Code 2025 - Day 05
import requests
from utils.vibes import printer

"""
# Debug printer function - now utils.vibes.printer is used instead
def printer_(msg):
    
    # check length and truncate if needed
    limit = 100
    if len(str(msg)) <= limit:
        trunk = str(msg)
    else:
        trunk = "Truncated after " + str(limit) + " characters\n\n" + str(msg)[0:limit]
    
    # build spool
    spool = "\n" + str(type(msg)) + "\nlength:" + str(len(msg)) + "\n\n" + str(trunk) + "\n\n"
    
    # if it's a list, also print types of elements
    if isinstance(msg, list):
        trunk_1 = []
        for i in msg:
            trunk_1.append(type(i))      
        trunked_1 = str(trunk_1)[0:limit]
        print(spool, f"{trunked_1}\n")
    else:
        print(spool)
"""

# For debugging, here's a sample input list
url_text = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

#  Get input data from GitHub, couldn't use Advent of Code site directly
url = "https://raw.githubusercontent.com/adambear82/advent-of-code/refs/heads/main/2025/day-05/input.txt"
resp = requests.get(url, timeout=10)
url_text = resp.text

# Split into two blocks on the blank line
str_fresh, str_food = url_text.strip().split("\n\n", 1)
str_fresh = str_fresh.splitlines()
str_food = str_food.splitlines()

# Parse "a-b" as integer tuples
fresh_ranges = []
for line in str_fresh:
    str_start, str_end = line.split("-")
    fresh_ranges.append((int(str_start), int(str_end)))

# Parse the food block as integers
num_food = [int(x) for x in str_food]

# simple - inefficient for large ranges
def in_any_range(num):
    return any(start <= num <= end for start, end in fresh_ranges)

# Optimized - ranges_list is expected to be fresh_ranges a list of start and end tuples
def is_in_any_range_efficient(num, ranges_list):
    for start, end in ranges_list:
        if start <= num <= end:
            return True
    return False


# initialize lists of fresh food
fresh = []

# Check each food number
for n in num_food:
    if in_any_range(n):
        fresh.append(n)

# part 1 - Get the length of fresh food list
length_fresh = len(fresh)

# part 1 result
print(f"Part 1 result (Fresh food count): {length_fresh}")

# part 2 - Get the min, max range that covers all fresh food
min_range = min(x[0] for x in fresh_ranges)
max_range = max(x[1] for x in fresh_ranges)
min_max = range(min_range, max_range + 1)

"""
# This is inefficient for large ranges, as it creates a massive list of integers.
fresh_all = []
# Check each number in the min-max range
printer(min_max)
for integers in min_max:
    #printer(integers)
    if in_any_range(integers):
        fresh_all.append(integers)
"""

# merge overlapping ranges to avoid large memory usage
def merge_ranges(ranges):
    if not ranges:
        return []
    ranges.sort()
    merged = [ranges[0]]
    for current_start, current_end in ranges[1:]:
        prev_start, prev_end = merged[-1]
        # If current range overlaps or is adjacent to the previous one, merge them
        if current_start <= prev_end + 1: 
            merged[-1] = (prev_start, max(prev_end, current_end))
        else:
            merged.append((current_start, current_end))
    return merged

merged_fresh_ranges = merge_ranges(fresh_ranges)

# Calculate total count of unique integers in the merged ranges
total_unique_fresh_count = 0
for start, end in merged_fresh_ranges:
    total_unique_fresh_count += (end - start + 1)

# part 2 result
print(f"Part 2 result (Total unique fresh count): {total_unique_fresh_count}")

printer(fresh_ranges)
