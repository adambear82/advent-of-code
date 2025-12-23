import sys
import os

# Add the parent directory to sys.path to resolve 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.vibes import get_raw

url_text = get_raw(day=1, year=2015)
url_text = url_text.strip()

def parens_to_ints(s: str) -> list[int]: # str -> list[int]
    """Map '(' -> +1 and ')' -> -1 for a given string."""
    mapping = {'(' : 1, ')' : -1} # mapping is a dictionary that maps '(' to +1 and ')' to -1
    return [mapping[ch] for ch in s] # return a list of the mapped values

output = parens_to_ints(url_text)

santa = 0

for index, value in enumerate(output):  # enumerate the list of values
    santa += value # santa's position is the sum of the values in the list
    print(f"[{index}] ► {value:+} ► {santa:02}") # print the current index, value, and santa's position
    if santa == -1: # if santa's position is -1, break
        break # break out of the loop

print(index)
