import sys
import os

# Add the parent directory to sys.path to resolve 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.vibes import get_raw
dash = "-" * 20

partone = """
┏━┓┏━┓┏━┓╺┳╸   ╻
┣━┛┣━┫┣┳┛ ┃    ┃
╹  ╹ ╹╹┗╸ ╹    ╹
"""

parttwo = """
┏━┓┏━┓┏━┓╺┳╸   ╻╻
┣━┛┣━┫┣┳┛ ┃    ┃┃
╹  ╹ ╹╹┗╸ ╹    ╹╹
"""

url_text = get_raw(day=5, year=2015)
url_text = url_text.strip().splitlines()
# url_text = url_text[:10]

# define constants to be used in checks
drop_consec = ["ab", "cd", "pq", "xy"]
vowels = ["a", "e", "i", "o", "u"]
keep_double = [chr(i) * 2 for i in range(ord('a'), ord('z') + 1)] # ['aa', 'bb', 'cc', etc]

# init empty lists
kept, dropped, check_consec, check_vowels, check_double = [], [], [], [], []

for i in url_text:
    
    # check for consecutive bad strings
    if any (drop_consec in i for drop_consec in drop_consec):
        check_consec.append("❌")
    else:
        check_consec.append("✔️")

    # check for at least 3 vowels
    count_vowels = sum(i.count(v) for v in vowels)
    if count_vowels < 3:
        check_vowels.append("❌")
    else:
        check_vowels.append("✔️")

    # check for double
    if any (keep_double in i for keep_double in keep_double):
        check_double.append("✔️")
    else:
        check_double.append("❌")

    # check for all conditions
    # [-1] is the latest element to be appended to the list
    if check_consec[-1] == "✔️" and check_vowels[-1] == "✔️" and check_double[-1] == "✔️":
        kept.append(i)
    else:
        dropped.append(i)

# print(dash)
# print("\n".join(url_text))
print(partone)
print(dash)
print(f"part 1 kept: {len(kept)}")
print(f"part 1 drop: {len(dropped)}")
print(dash)



# init empty lists for Part 2 checks and results
kept, dropped = [], [] # reset kept and dropped lists for Part 2
check_pair_twice, check_repeat_gap1 = [], [] # create new empty lists for Part 2 checks

for i in url_text:
    # Rule A: pair of two letters that appears at least twice without overlapping
    has_pair_twice = False
    # Scan all two-letter windows and see if it appears again later (starting at i+2 to avoid overlap)
    for j in range(len(i) - 1):
        pair = i[j:j+2]
        if pair and pair in i[j+2:]:
            has_pair_twice = True
            break

    if has_pair_twice:
        check_pair_twice.append("✔️")
    else:
        check_pair_twice.append("❌")

    # Rule B: letter repeats with exactly one letter between (pattern: x_x)
    has_repeat_gap1 = False
    for j in range(len(i) - 2):
        if i[j] == i[j+2]:
            has_repeat_gap1 = True
            break

    if has_repeat_gap1:
        check_repeat_gap1.append("✔️")
    else:
        check_repeat_gap1.append("❌")

    # Final decision for Part 2: both rules must be satisfied
    # [-1] is the latest element to be appended to the list
    if check_pair_twice[-1] == "✔️" and check_repeat_gap1[-1] == "✔️":
        kept.append(i)
    else:
        dropped.append(i)

print(parttwo)
print(dash)
print(f"part 2 kept: {len(kept)}")
print(f"part 2 drop: {len(dropped)}")
print(dash)

