# -------- boilerplate -------- 

import sys, os#, itertools
# from tabulate import tabulate # sudo apt install python3-tabulate
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe# dash, dec_print, prints

# --------- definitions ---------

def top_five_letters_joined(strings):
    results = []
    for s in strings:
        freq = {}

        # Count characters manually
        for ch in s:
            freq[ch] = freq.get(ch, 0) + 1

        # Sort by: frequency desc, then letter asc
        sorted_letters = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

        # Extract letters only (top 5)
        top5 = [letter for letter, count in sorted_letters[:5]]

        # Join into a single string
        results.append("".join(top5))

    return results



def decrypt_name(room, index=None):
    # If given a list, process each item WITH its index
    if isinstance(room, list):
        return [decrypt_name(r, i) for i, r in enumerate(room)]

    # Process a single encrypted room string
    parts = room.split("-")

    # Extract sector ID
    sector_id = int(parts[-2])

    # Everything except last 2 parts (sector + checksum)
    encrypted = "-".join(parts[:-2])

    # Caesar shift
    shift = sector_id % 26

    result = []
    for ch in encrypted:
        if ch == "-":
            result.append(" ")
        else:
            new_pos = (ord(ch) - ord('a') + shift) % 26
            result.append(chr(ord('a') + new_pos))

    decrypted = "".join(result)

    # Return (index, decrypted_name)
    return (index, decrypted)


def find_room_index(rooms, target):
    for idx, name in rooms:
        if name == target:
            return idx
    return None


# -------- main -----------------

wipe()
part(8)

rooms0 = get_raw(day=4, year=2016, file_name="input.txt")
rooms1 = rooms0.strip().split("\n")
print(f"input.txt {rooms1[:4] = }...\n")
rooms2 = [r.replace("[", "-").replace("]", "") for r in rooms1]
print(f"{rooms2[:4] = }...\n")
rooms3 = [r.split("-") for r in rooms2]

checksums = [r[-1] for r in rooms3]
print(f"{checksums[:4] = }...\n")

all_sector_ids = [int(r[-2]) for r in rooms3]
print(f"{all_sector_ids[:4] = }...\n")
print(f"{sum(all_sector_ids) = }\n")


rooms4 = [[ "".join(r[:-2])] for r in rooms3]
rooms5 = [x for row in rooms4 for x in row]
print(f"joined and sorted {rooms5[:4] = }...\n")

part(9)

top_five = top_five_letters_joined(rooms5)

print(f"{top_five[:4] = }\n")

valid_sector_ids = []
match = []
for n, (a, b, s) in enumerate(zip(checksums, top_five, all_sector_ids)):
    if a == b :
        match.append([n, a == b, a, b])
        valid_sector_ids.append(s)

print(f"{match[:4] = }...\n")
print(f"{valid_sector_ids[:4] = }....")

part(1)
print(f"{sum(valid_sector_ids) = }")

part(2)
dycrypted = decrypt_name(rooms2)

search_term = "northpole object storage"
index_of_searched_room = find_room_index(dycrypted, search_term)
print(f"{search_term = }")
print(f"{index_of_searched_room = }")
print(f"{all_sector_ids[299] = }\n")

# print(dycrypted[298:302])
# for item in dycrypted :
#     print(f"{item},")
