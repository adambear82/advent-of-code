# Advent of Code 2025 - Day 01
import requests

# Get input data from GitHub, couldn't use Advent of Code site directly
url = "https://raw.githubusercontent.com/adambear82/advent-of-code/refs/heads/main/2025/day-01/input.txt"
resp = requests.get(url, timeout=10)
LR = resp.text.strip().splitlines()

# initialize variables
counter = 0
dial = 1050
moves = []

# replace L with negative sign and R with nothing to convert to signed integers
for lr in LR :
    signed_str = lr.replace('L', '-').replace('R', '')
    moves.append(int(signed_str))

# this print is ony useful for debugging, there are too many moves to see them all
print ("the dial starts by pointing to", dial)

# process each move, updating the dial and counting multiples of 100, using modulo
for m in moves :
    dial += m
    print (dial)
    if dial % 100 == 0 :
        counter += 1

# final output
print("The dial landed on a multiple of 100 a total of", counter, "times.")
