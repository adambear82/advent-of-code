import sys, os, platform
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe

import json
from numbers import Number

# -------------------------------------------

def extract_numbers(obj):
    """
    Recursively collect numeric values (int/float/etc.) from nested dicts/lists/tuples/sets.
    - Accepts a Python dict/list OR a JSON string and parses it.
    - Excludes booleans (bool is a subclass of int).
    """
    # If it's a string, try to parse as JSON
    if isinstance(obj, str):
        try:
            obj = json.loads(obj)
        except json.JSONDecodeError:
            # Not valid JSON; no numbers to extract from raw strings
            return []

    result = []

    def walk(x):
        if isinstance(x, bool):
            return
        if isinstance(x, Number):
            result.append(x)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, (list, tuple, set)):
            for item in x:
                walk(item)
        # Other types are ignored

    walk(obj)
    return result


def extract_red(obj):
    """
    Recursively collect numeric values (int/float/etc.) from nested dicts/lists/tuples/sets.
    - Accepts a Python dict/list OR a JSON string and parses it.
    - Excludes booleans (bool is a subclass of int).
    """
    # If it's a string, try to parse as JSON
    if isinstance(obj, str):
        try:
            obj = json.loads(obj)
        except json.JSONDecodeError:
            # Not valid JSON; no numbers to extract from raw strings
            return []

    result = []

    def walk(x):

        if isinstance(x, bool):
            return

        if isinstance(x, Number):
            result.append(x)
            return

        elif isinstance(x, dict): # we only care if a dictionary
            if "red" in x.values(): # it must have a value of "red"
                return # if it does, we skip it
            else: # otherwise we extract the numbers
                for v in x.values(): # for each value
                    walk(v) # we walk it *iteratively*

        elif isinstance(x, (list, tuple, set)):
            for item in x:
                walk(item)

        # Other types are ignored

    walk(obj)
    return result

# -------------------------------------------

wipe()

part(1)

print("first 1000 chars of part 1 input:\n")
input_txt = get_raw(day=12, year=2015, file_name="input.txt")
INPUT_TXT = input_txt[:1000]
print(INPUT_TXT)

extracted = extract_numbers(input_txt)
EXTRACTED = extracted[:10]
print(f"\nfirst 10 numbers extracted from full input:\n\n{EXTRACTED}\n")

sum_extracted = sum(extracted)
print(f"sum of extracted: {sum_extracted}\n")

part(2)

extracted_red = extract_red(input_txt)
EXTRACTED_RED = extracted_red[:10]
print(f"first 10 numbers extracted from full input:\n\n{EXTRACTED_RED}\n")

sum_extracted_red = sum(extracted_red)
print(f"sum of extracted: {sum_extracted_red}\n")
