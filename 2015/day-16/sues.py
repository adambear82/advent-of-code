import sys, os
from tabulate import tabulate # sudo apt install python3-tabulate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe, dash


#--------- definitions ---------
def list_to_dict(input_list):
    result = {}

    for line in input_list:
        # Split "Sue <num>" from the rest
        left, right = line.split(": ", 1)

        # Extract the sue number (as int)
        sue_num = int(left.split()[1])

        # Parse the attribute list
        attributes = {}
        for part in right.split(","):
            key, value = part.strip().split(": ")
            attributes[key] = int(value)

        # Store in dictionary
        result[sue_num] = attributes

    return result

def dict_to_rows_ordered(data):
    """
    Build rows and headers so that:
    - Attributes (columns) are in alphabetical order
    - 'Sue' column comes first
    - All rows share the same columns (missing attrs shown as '')
    - Sues are sorted numerically
    """
    # 1) Collect the union of all attribute names across all Sues
    all_attrs = set()
    for attrs in data.values():
        all_attrs.update(attrs.keys())

    # 2) Build headers with 'Sue' first, then attributes alphabetically
    headers = ["Sue"] + sorted(all_attrs)

    # 3) Build rows in that exact key order
    rows = []
    for sue in sorted(data.keys()):  # numeric order of Sue IDs
        attrs = data[sue]
        row = {"Sue": sue}
        # Insert attribute keys in alphabetical order
        for a in sorted(all_attrs):
            row[a] = attrs.get(a, "")  # or 0 if you prefer numeric blanks
        rows.append(row)

    return rows, headers

def check_sue(sue_dict, mfcsam_dict):
    mfcsam_dict = mfcsam_dict[0] # use first and only item in mfcsam_dict
    """
    Check each Sue against the MFCSAM.
    Returns a list of matching Sue numbers.
    """
    matches = [] # init list to store matching sue numbers

    for sue_num, sue_attrs in sue_dict.items(): # iterate through each sue
        is_match = True # assume match until proven otherwise

        for attr, value in sue_attrs.items(): # iterate through each attribute of the current sue
            
            # if the attribute is not in the MFCSAM
            """ 
            if attr not in mfcsam_dict: # if the attribute is not in the MFCSAM
                
                is_match = False # Sue has an unknown attribute → not a match
                break # break the inner loop
            """

            # if the value of the attribute is not equal to the value of the attribute in the MFCSAM
            if value != mfcsam_dict[attr]:
                is_match = False # Value mismatch → not a match
                break # break the inner loop

        if is_match: # if the sue is a match
            matches.append(sue_num) # add the sue number to the list of matches

    return matches

# --------- main ---------
wipe()
part(9)

mfcsam = get_raw(day=16, year=2015, file_name="mfcsam.txt").strip().splitlines()
mfcsam_dict = list_to_dict(mfcsam)
mfcsam_rows, headers = dict_to_rows_ordered(mfcsam_dict)
tab_fmt = "rounded_outline"
tab_mfc = tabulate(mfcsam_rows,  headers="keys", tablefmt=tab_fmt)
print(tab_mfc)

part(8)

input_txt = get_raw(day=16, year=2015, file_name="input.txt").strip().splitlines()
sue_dict = list_to_dict(input_txt)
sue_rows, headers = dict_to_rows_ordered(sue_dict)

ans = 40
slice = 3
trunk = "\n/////TRUNCATED/////\n"

tab_0 = tabulate(sue_rows[:slice],  headers="keys", tablefmt=tab_fmt)
tab_1 = tabulate(sue_rows[ans-1:ans],   headers="keys", tablefmt=tab_fmt)
tab_2 = tabulate(sue_rows[-slice:], headers="keys", tablefmt=tab_fmt)

print(tab_0, trunk, tab_1, trunk, tab_2, sep="\n")

part(1)

checked = check_sue(sue_dict, mfcsam_dict)
print(f"The correct Sue is: {checked}\n")
