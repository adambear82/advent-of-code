# Advent of Code 2025 - Day 01
import requests
import re

#  Get input data from GitHub, couldn't use Advent of Code site directly
url = "https://raw.githubusercontent.com/adambear82/advent-of-code/refs/heads/main/2025/day-02/input.txt"
resp = requests.get(url, timeout=10)
url_text = resp.text.strip()

# For debugging, here's a sample input string
# url_text = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

# use regular expression to split on '-' and ',' and slice
splat = re.split(r'[-,]', url_text)
id_start = splat[0::2]
id_end = splat[1::2]

# initialize variables
id = []
errors = []
error_sum = 0

# convert to int, process each range and create list of lists
for i in range(len(id_start)) :
    start = int(id_start[i])
    end = int(id_end[i])
    i_ranges = list(range(start, end+1))
    id.append(i_ranges)

# flatten as we dont care where an error was
id = [item for sublist in id for item in sublist]

# part 1 - check for even number of digits and 1st half = 2nd
def check_valid_part1(num):
    str_num = str(num)
    if len(str_num) % 2 != 0:
        return False
    half = len(str_num) // 2
    if str_num[:half] == str_num[half:] :
        int_num = int(str_num)
        errors.append(int_num)

# part 2 - check for any chunk size that repeats
def check_valid_part2(num):
    str_num = str(num)
    length = len(str_num)
    for chunk_size in range(1, length // 2 + 1):
        if length % chunk_size == 0:  # Must divide evenly
            chunk = str_num[:chunk_size]
            if chunk * (length // chunk_size) == str_num:
                int_num = int(str_num)
                errors.append(int_num)
                break  # No need to check 222-222 after 22-22-22

# process each ID in the list
for i in id:
    check_valid_part2(i)

# sum up the errors    
for e in errors:
    error_sum += e

# part 1 output
print(f"""
The invalid IDs are:
{errors}

And the sum of all invalid IDs is:
{error_sum}
""")
