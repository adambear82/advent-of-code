# -------- boilerplate -------- 

import sys, os#, itertools
from tabulate import tabulate # sudo apt install python3-tabulate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe, dash, dec_print, prints

# --------- definitions ---------

def sum(list):
    total = 0
    for i in list:
        total += i
    return total

def third(sum):
    return (sum // 3) # double slashes // indicate integer division

import itertools
import math

def three_partitions(nums, top_n=1):
    total = sum(nums)
    if total % 3 != 0:
        return []

    target = total // 3
    nums = sorted(nums, reverse=True)

    all_solutions = []

    # STEP 1: find smallest-size group1 subsets first
    for size in range(1, len(nums)):
        for combo in itertools.combinations(nums, size):
            if sum(combo) == target:
                qe = math.prod(combo)
                all_solutions.append((combo, qe))

        if all_solutions:
            break  # stop after the FIRST size that works

    # STEP 2: sort by QE (smallest first)
    all_solutions.sort(key=lambda x: x[1])

    results = []

    # STEP 3: validate remaining two groups
    for group1, qe in all_solutions:
        if len(results) >= top_n:
            break

        remaining = nums.copy()
        for x in group1:
            remaining.remove(x)

        # Now find a group2 that sums to target
        found_group2 = False
        for size in range(1, len(remaining)):
            for combo2 in itertools.combinations(remaining, size):
                if sum(combo2) == target:
                    # Group3 is everything left
                    group3 = remaining.copy()
                    for x in combo2:
                        group3.remove(x)

                    if sum(group3) == target:
                        results.append((list(group1), list(combo2), list(group3), qe))
                        found_group2 = True
                        break
            if found_group2:
                break

    return results

# -------- main -----------------

wipe()
part(9)

example_data = get_raw(day=24, year=2015, file_name="example.txt")
example_data = example_data.strip().split("\n")
example_data = [int(x) for x in example_data]

print(f"{example_data = }")
print(f"{sum ( example_data ) = }")
print(f"{third ( sum ( example_data ) ) = }\n")

for a, b, c, qe in three_partitions(example_data):
    print(a, b, c, "QE = ", qe)

part(8)

real_data = get_raw(day=24, year=2015, file_name="input.txt")
real_data = real_data.strip().split("\n")
real_data = [int(x) for x in real_data]

print(f"{real_data = }\n")
print(f"{sum ( real_data ) = }\n")
print(f"{third ( sum ( real_data ) ) = }\n")

part(1)

for a, b, c, qe in three_partitions(real_data):
    print(a, b, c, "QE = ", qe)
