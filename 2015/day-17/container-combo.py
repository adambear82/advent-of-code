import sys, os, itertools
from tabulate import tabulate # sudo apt install python3-tabulate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe, dash, prints

#--------- definitions ---------

def find_combinations(containers, target):
    """
    Find all combinations (any size) of containers that sum to the target.
    Treats identical-sized containers as distinct choices (by index).
    """
    combinations = []
    n = len(containers)
    for r in range(1, n + 1):
        for combo in itertools.combinations(containers, r):
            if sum(combo) == target:
                combinations.append(combo)

    # prints(f"{combinations} # combinations")
    prints(f"{len(combinations)} # number of combinations\n")
    
    len_comb = []
    for c in combinations:
        len_comb.append(len(c))
    prints(f"{len_comb} # length of combinations\n")

    min_len = min(len_comb)
    prints(f"{min_len} # minimum length of combinations\n")
    
    min_comb = []
    for c in combinations:
        if len(c) == min_len:
            min_comb.append(c)
    prints(f"{min_comb} # minimum length combinations\n")
    prints(f"{len(min_comb)} # number of minimum length combinations\n")

# --------- example ---------
wipe()
part(9)

example_containers = [20, 15, 10, 5, 5] # already ints
example_target = 25

prints(f"{example_containers} # example containers")
prints(f"{example_target} # example target\n")

find_combinations(example_containers, example_target)

# --------- main ---------

part(8)

containers = get_raw(day=17, year=2015, file_name="input.txt").strip().splitlines()
int_containers = [int(x) for x in containers] # cast to int
sorted_containers = sorted(int_containers, reverse=True)
target = 150

prints(f"{containers} # containers")
prints(f"{sorted_containers} # sorted containers")
prints(f"{target} # target\n")

part(1)

find_combinations(sorted_containers, target)


