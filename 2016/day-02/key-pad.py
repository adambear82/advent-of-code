# -------- boilerplate -------- 

import sys, os#, itertools
from tabulate import tabulate # sudo apt install python3-tabulate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe, dash, dec_print, prints

# --------- definitions ---------

def num_pad(seq) :
    pos = 1
    code = []
    for s in seq :
        for d in s :
            
            if pos == 1 :
                if   d == "U" : pos = 1
                elif d == "D" : pos = 4
                elif d == "L" : pos = 1
                elif d == "R" : pos = 2

            elif pos == 2 :
                if   d == "U" : pos = 2
                elif d == "D" : pos = 5
                elif d == "L" : pos = 1
                elif d == "R" : pos = 3

            elif pos == 3 :
                if   d == "U" : pos = 3
                elif d == "D" : pos = 6
                elif d == "L" : pos = 2
                elif d == "R" : pos = 3

            elif pos == 4 :
                if   d == "U" : pos = 1
                elif d == "D" : pos = 7
                elif d == "L" : pos = 4
                elif d == "R" : pos = 5

            elif pos == 5 :
                if   d == "U" : pos = 2
                elif d == "D" : pos = 8
                elif d == "L" : pos = 4
                elif d == "R" : pos = 6

            elif pos == 6 :
                if   d == "U" : pos = 3
                elif d == "D" : pos = 9
                elif d == "L" : pos = 5
                elif d == "R" : pos = 6
            
            elif pos == 7 :
                if   d == "U" : pos = 4
                elif d == "D" : pos = 7
                elif d == "L" : pos = 7
                elif d == "R" : pos = 8

            elif pos == 8 :
                if   d == "U" : pos = 5
                elif d == "D" : pos = 8
                elif d == "L" : pos = 7
                elif d == "R" : pos = 9

            elif pos == 9 :
                if   d == "U" : pos = 6
                elif d == "D" : pos = 9
                elif d == "L" : pos = 8
                elif d == "R" : pos = 9
                        
        code.append(pos)
    return code

def num_pad_dic(seq):
    transitions = {
        "1": {"U": "1", "D": "3", "L": "1", "R": "1"},
        "2": {"U": "2", "D": "6", "L": "2", "R": "3"},
        "3": {"U": "1", "D": "7", "L": "2", "R": "4"},
        "4": {"U": "4", "D": "8", "L": "3", "R": "4"},
        "5": {"U": "5", "D": "5", "L": "5", "R": "6"},
        "6": {"U": "2", "D": "A", "L": "5", "R": "7"},
        "7": {"U": "3", "D": "B", "L": "6", "R": "8"},
        "8": {"U": "4", "D": "C", "L": "7", "R": "9"},
        "9": {"U": "9", "D": "9", "L": "8", "R": "9"},
        "A": {"U": "6", "D": "A", "L": "A", "R": "B"},
        "B": {"U": "7", "D": "D", "L": "A", "R": "C"},
        "C": {"U": "8", "D": "C", "L": "B", "R": "C"},
        "D": {"U": "B", "D": "D", "L": "D", "R": "D"},
    }

    pos = "5"
    code = []

    for s in seq:
        for d in s:
            pos = transitions[pos][d]
        code.append(pos)

    return code

# -------- main -----------------

wipe()
part(9)

print(num_pad(["ULL","RRDDD","LURDL","UUUUD"]))

part(8)

seq = get_raw(day=2, year=2016, file_name="input.txt")
seq = seq.strip().split("\n")
print(seq)

part(1)
print(num_pad(seq))

part(2)
print(num_pad_dic(seq))
print()
