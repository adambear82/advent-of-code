
import sys, os, platform
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe

import re
import itertools
from copy import deepcopy

# -------------------------------------------------------------

def format_happiness(lines):
    """
    Parse lines of the form:
    '<A> would gain|lose <N> happiness units by sitting next to <B>.'
    
    Returns a list of [personA, personB, happinessDelta] where happinessDelta
    is positive for 'gain' and negative for 'lose'.
    """
    pattern = re.compile(
        r"^(\w+)\s+would\s+(gain|lose)\s+(\d+)\s+happiness\s+units\s+by\s+sitting\s+next\s+to\s+(\w+)\.$",
        re.IGNORECASE
    )
    
    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        m = pattern.match(line)
        if not m:
            raise ValueError(f"Line does not match expected format: {line}")
        
        person_a, verb, units_str, person_b = m.groups()
        units = int(units_str)
        if verb.lower() == "lose":
            units = -units
        
        results.append([person_a, person_b, units])
    
    return results


def build_happiness_map(entries):
    """
    entries: list of [A, B, delta]
    Returns:
      h: dict of dicts {A: {B: delta, ...}, ...} (directed)
      people: sorted list of unique people
    """
    h = {}
    people = set()
    for a, b, delta in entries:
        if a not in h:
            h[a] = {}
        h[a][b] = delta
        people.add(a)
        people.add(b)
    return h, sorted(people)


def total_happiness_circle(order, h):
    """
    Sum happiness around a circular table for a given seating order (tuple/list).
    For each adjacent unordered pair (a, b), add h[a][b] + h[b][a].
    Missing directed entries default to 0 (useful for Part 2 with 'You').
    """
    n = len(order)
    total = 0
    for i in range(n):
        a = order[i]
        b = order[(i + 1) % n]  # wrap-around
        total += h.get(a, {}).get(b, 0)
        total += h.get(b, {}).get(a, 0)
    return total


def best_arrangement(people, h):
    """
    Find the maximum total happiness over all circular seatings.
    Anchor the first person to break rotational symmetry.
    Returns: (best_score, best_route)
    """
    if not people:
        return 0, tuple()
    first = people[0]
    rest = people[1:]
    best_score = None
    best_route = None
    for perm in itertools.permutations(rest):
        route = (first,) + perm
        score = total_happiness_circle(route, h)
        if (best_score is None) or (score > best_score):
            best_score = score
            best_route = route
    return best_score, best_route


def add_neutral_person(h, people, name="You"):
    """
    Add a neutral person with 0 happiness change with everyone in both directions.
    Returns updated (h, people_list).
    """
    if name in people:
        return h, people
    # Ensure existing people can look up 'name' as neighbor with 0.
    for p in people:
        h.setdefault(p, {})[name] = 0
    # 'name' looks at all others with 0.
    h[name] = {p: 0 for p in people}
    new_people = list(people) + [name]
    return h, new_people

# -------------------------------------------------------------

wipe()

# ---------------- Example ----------------
print("example input:\n")
example_txt = get_raw(day=13, year=2015, file_name="example.txt").strip().splitlines()
example_preview = example_txt[:5]
print("\n".join(example_preview))

formatted = format_happiness(example_txt)
print(f"\nexample structure (first up to 5 entries):\n\n{formatted[:5]}")

h_ex, people_ex = build_happiness_map(formatted)
score_ex_p1, route_ex_p1 = best_arrangement(people_ex, h_ex)
print(f"\n[Example] Part 1 max happiness: {score_ex_p1}")
print(f"\n[Example] Part 1 best route:\n\n{route_ex_p1}")

# Expect 330 for the AoC example (as a quick sanity check).

"""
# Part 2 on example: add 'You' with 0 happiness both directions
h_ex_p2 = deepcopy(h_ex)
h_ex_p2, people_ex_p2 = add_neutral_person(h_ex_p2, people_ex, name="You")
score_ex_p2, route_ex_p2 = best_arrangement(people_ex_p2, h_ex_p2)
print(f"\n[Example] Part 2 max happiness (with 'You'): {score_ex_p2}")
print(f"\n[Example] Part 2 best route:\n\n{route_ex_p2}")
"""
# ---------------- Real Input ----------------

part(1)

raw = get_raw(day=13, year=2015).strip().splitlines()
entries = format_happiness(raw)
h, people = build_happiness_map(entries)

ans1, route1 = best_arrangement(people, h)
print(f"[Input] Part 1 max happiness: {ans1}")
print(f"[Input] Part 1 best route: {route1}\n")

print(ans1)

part(2)

h2 = deepcopy(h)
h2, people2 = add_neutral_person(h2, people, name="You")
ans2, route2 = best_arrangement(people2, h2)
print(f"\n[Input] Part 2 max happiness (with 'You'): {ans2}")
print(f"[Input] Part 2 best route:\n\n{route2}\n")

print(ans2)
