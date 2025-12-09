import math
from utils.vibes import get_raw  # type: ignore
from utils.blackbox import parse_cephalopod_worksheet  # type: ignore

# sample input for testing
url_text = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

url_text = get_raw(6)

# process input as text
row = url_text.splitlines()              # ['123 328  51 64',
splat = [line.split() for line in row]   # [['123', '328', '51', '64'],
operators = splat.pop()                  # ['*', '+', '*', '+']

# convert to integers and transpose
nums = [[int(num_str) for num_str in row] for row in splat] # [[123, 328, 51, 64],
trans_tuples = zip(*nums)                                   # <zip object at ...>
trans_list = [list(row) for row in trans_tuples]            # [[123, 45, 6],

# init variables
worksheet_1 = []
worksheet_2 = []

# use zip to pair each transposed row with its operator
for row, op in zip(trans_list, operators):
    if op == '+':
        worksheet_1.append(sum(row))

    elif op == '*':
        worksheet_1.append(math.prod(row))
sum_sheet_1 = sum(worksheet_1)

# part 1 result
print(f"\nPart 1 result\nSum of worksheet_1\n{sum_sheet_1}\n")

# Parsed numbers grouped by problem Right to Left order)
cepha_cypher = parse_cephalopod_worksheet(url_text)

# reverse operators for Right to Left processing
reverse_operators = operators[::-1]

# use zip to pair each transposed row with its operator
for row, op in zip(cepha_cypher, reverse_operators):
    if op == '+':
        worksheet_2.append(sum(row))
        # print(sum(row))

    elif op == '*':
        worksheet_2.append(math.prod(row))
        # print(math.prod(row))
sum_sheet_2 = sum(worksheet_2)

# part 2 result
print(f"Part 2 result\nSum of worksheet_2\n{sum_sheet_2}\n")
