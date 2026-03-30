# -------- boilerplate -------- 
from collections import Counter
import sys, os#, itertools
# from tabulate import tabulate # sudo apt install python3-tabulate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe# dash, dec_print, prints

# --------- definitions ---------

def trans_code (input) :
    result = ""

    for tup in input :
        counts = Counter(tup)
        most_common_letter = counts.most_common(1)[0][0]
        result += most_common_letter
    
    return result

def trans_code_least (input) :
    result = ""

    for tup in input :
        counts = Counter(tup)
        # least common is the LAST element in most_common()
        least_common_letter = counts.most_common()[-1][0]
        result += least_common_letter
    
    return result

# -------- main -----------

wipe()
part(8)

example = get_raw(day=6, year=2016, file_name="example.txt")
example_strip = example.strip().split("\n")
print(f"{example_strip = }\n")

example_trans = list(zip(*example_strip))
print(f"{example_trans = }")

part(9)

decoded = trans_code(example_trans)
print(f"{decoded = }")

decoded_least = trans_code_least(example_trans)
print(f"{decoded_least = }")

part(1)

input = get_raw(day=6, year=2016, file_name="input.txt")
input_strip = input.strip().split("\n")
input_strip_sliced = input_strip[:4]
print(f"{input_strip_sliced = }\n")

input_trans = list(zip(*input_strip))
input_trans_sliced = input_trans[:1]
print(f"{input_trans_sliced = }\n")

decoded_input = trans_code(input_trans)
print(f"{decoded_input = }\n")

part(2)

decoded_input_least = trans_code_least(input_trans)
print(f"{decoded_input_least = }\n")
