import sys, os, platform
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe

import re

# ------------ Definitions Start-----------

def format_deer(lines):
    """
    Parse lines of the form:
    '<D> can fly <S> km/s for <F> seconds, but then must rest for <R> seconds.'
    
    Returns a list of [deer, speed, fly_time, rest_time].
    """
    pattern = re.compile(
        r"^(\w+)\s+can\s+fly\s+(\d+)\s+km/s\s+for\s+(\d+)\s+seconds,\s+but\s+then\s+must\s+rest\s+for\s+(\d+)\s+seconds.$",
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
        
        deer, speed, fly_time, rest_time = m.groups()
        speed = int(speed)
        fly_time = int(fly_time)
        rest_time = int(rest_time)
        
        results.append([deer, speed, fly_time, rest_time])
    
    return results

def format_units():
    print("units:\ndeer name, speed, fly time, rest time\n")

def race_deer(input_txt, race_time):
    """
    Simulate a race where each deer runs at its constant speed for the given amount of time.
    Returns a list of [deer, distance] for each deer.
    """
    results = []
    for deer, speed, fly_time, rest_time in input_txt:
        cycles = race_time // (fly_time + rest_time)
        remaining_time = race_time % (fly_time + rest_time)
        
        distance = cycles * fly_time * speed
        distance += min(remaining_time, fly_time) * speed
        
        results.append([deer, distance])
    
    return sorted(results, key=lambda x: x[1], reverse=True)


def race_deer_points(input_txt, race_time):
    """
    Simulate the race second-by-second and award points:
    - Each second, any deer at the max distance gets 1 point.
    - Return a list of [deer, points].
    """
    # Initialize trackers
    distances = {deer: 0 for deer, _, _, _ in input_txt}
    points = {deer: 0 for deer, _, _, _ in input_txt}

    for s in range(1, race_time + 1):
        # Update distances for this second
        for deer, speed, fly_time, rest_time in input_txt:
            cycle = fly_time + rest_time
            # Deer is flying for the first `fly_time` seconds of each cycle
            if (s - 1) % cycle < fly_time:
                distances[deer] += speed

        # Find leaders and award points
        lead_dist = max(distances.values())
        for deer in distances:
            if distances[deer] == lead_dist:
                points[deer] += 1

    result = [[deer, points[deer]] for deer in points]
    return sorted(result, key=lambda x: x[1], reverse=True)

# ---------------- Part 0  ----------------

wipe()
part(9)

file_name = "example.txt"

print("example input:\n")
example_txt = get_raw(day=14, year=2015, file_name=file_name).strip().splitlines()
example_preview = example_txt#[:2]
print("\n".join(example_preview))

example_list = format_deer(example_preview)
print(f"\nexample list:\n\n{example_list}\n")

format_units()

example_formatted = "\n".join(", ".join(map(str, row)) for row in example_list)
print(f"example formatted:\n\n{example_formatted}\n")

example_race = race_deer(example_list, 1000)
race_formatted = "\n".join(", ".join(map(str, row)) for row in example_race)
print(f"example sorted race results:\n\n{race_formatted}\n")

# ---------------- Part 1 ----------------
part(8)

file_name = "input.txt"
race_length = 2503
preview_slice = slice(None, 3)

print("part 1 input:\n")
input_txt = get_raw(day=14, year=2015, file_name=file_name).strip().splitlines()
input_preview = input_txt[preview_slice]
print("\n".join(input_preview))

input_list = format_deer(input_txt)
print(f"\ninput list:\n\n{input_list[preview_slice]}\n")

format_units()

input_formatted = "\n".join(", ".join(map(str, row)) for row in input_list)
print(f"input formatted:\n\n{input_formatted}\n")

part(1)

input_race = race_deer(input_list, race_length)
race_formatted = "\n".join(", ".join(map(str, row)) for row in input_race)
print(f"sorted results:\n\n{race_formatted}\n")

print(f"part 1 answer: {input_race[0]}")

# ---------------- Part 2 ----------------
part(2)

PART2_RACE_TIME = 2503  # AoC 2015 Day 14 uses 2503 seconds for the puzzle input

input_points = race_deer_points(input_list, PART2_RACE_TIME)
input_points_formatted = "\n".join(", ".join(map(str, row)) for row in input_points)
print(f"input points sorted results:\n\n{input_points_formatted}\n")

print(f"part 2 answer: {input_points[0]}")


