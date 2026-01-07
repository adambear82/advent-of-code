import sys, os, platform
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe

import itertools
# --------------------------------------------------------------

def edge_key(a, b):
    """Return a consistent key like 'CityA-CityB' regardless of order."""
    if a < b:
        return a + "-" + b
    else:
        return b + "-" + a

def parse_input(lines):
    edges = {}
    cities = set()

    for line in lines:
        # Example line: "London to Dublin = 464"
        parts = line.split()
        city1 = parts[0]
        city2 = parts[2]
        distance = int(parts[4])

        key = edge_key(city1, city2)
        edges[key] = distance

        cities.add(city1)
        cities.add(city2)

    return edges, list(cities)

def route_distance(route, edges):
    total = 0
    for i in range(len(route) - 1):
        a = route[i]
        b = route[i + 1]
        key = edge_key(a, b)
        total += edges[key]
    return total

def find_shortest_and_longest(edges, cities):
    shortest = None
    longest = None

    for route in itertools.permutations(cities):
        d = route_distance(route, edges)

        if shortest is None or d < shortest:
            shortest = d
            shortest_route = route

        if longest is None or d > longest:
            longest = d
            longest_route = route

    return shortest, longest, shortest_route, longest_route

# --------------------------------------------------------------

wipe()

print("example input:\n")
example_txt = get_raw(day=9, year=2015, file_name="example.txt")
example_txt = example_txt.strip().splitlines()
example_preview = example_txt
example_joined = "\n".join(example_preview)
print(example_joined,"\n")

edges, cities = parse_input(example_txt)
shortest, longest, shortest_route, longest_route = find_shortest_and_longest(edges, cities)

print(f"edges are codified inputs:\n{edges}\n\ncities are unique:\n{cities}\n")

print(f"Shortest route: {shortest}\n{shortest_route}\n")
print(f"Longest route: {longest}\n{longest_route}\n")

part(1)

print("first 10 lines of input:\n")
input_txt = get_raw(day=9, year=2015)
input_txt = input_txt.strip().splitlines()
input_preview = input_txt[:10]
input_joined = "\n".join(input_preview)
print(input_joined, "\n")

edges, cities = parse_input(input_txt)
shortest, longest, shortest_route, longest_route = find_shortest_and_longest(edges, cities)

print(f"Shortest route: {shortest}\n\n{shortest_route}")

part(2)

print(f"Longest route: {longest}\n\n{longest_route}\n")
