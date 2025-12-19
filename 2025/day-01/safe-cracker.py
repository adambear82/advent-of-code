# Advent of Code 2025 - Day 01
import requests

# Get input data from GitHub, couldn't use Advent of Code site directly
url = "https://raw.githubusercontent.com/adambear82/advent-of-code/refs/heads/main/2025/day-01/input.txt"
resp = requests.get(url, timeout=10)

LR = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""
LR = LR.strip().splitlines()
#LR = LR[:2]

LR = resp.text.strip().splitlines()

# initialize variables
part1_counter, part2_counter = 0, 0
dial = 1050
moves = []

# replace L with negative sign and R with nothing to convert to signed integers
for lr in LR :
    signed_str = lr.replace('L', '-').replace('R', '')
    moves.append(int(signed_str))

# this print is ony useful for debugging, there are too many moves to see them all
print (f"\nthe dial starts by pointing to :\n{dial}")
print (f"\nthe moves are :\n{moves}\n")
# part 1 output for counting dial at rest

# process each move, updating the dial and counting multiples of 100, using modulo
for m in moves :
    dial += m
    print (dial)
    if dial % 100 == 0 :
        part1_counter += 1

# final output
print(f"\nThe dial landed on a multiple of 100 a total of {part1_counter} times.\n")


# part 2 output for counting dial in motion
# process each move, updating the dial and counting multiples of 100, using modulo
for m in moves :
    print("-" * 20)
    print(m)
    if m < 0 :
        print("negative\n")
        clicks = [-1 for _ in range(abs(m))]
    else :
        print("positive\n")
        clicks = [1 for _ in range(m)]
    print(clicks)

    for c in clicks :
        dial += c
        print (dial)
        if dial % 100 == 0 :
            part2_counter += 1
            print("*" * 5, part2_counter)


# final output
print("-" * 20)
print(f"\nThe dial landed on a multiple of 100 a total of {part1_counter} times.\n")

print(f"\nThe dial passed through a multiple of 100 a total of {part2_counter} times.\n")

