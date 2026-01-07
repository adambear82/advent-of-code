import sys, os, platform
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.vibes import get_raw, part, wipe

# --------------------------------------------------------------

def escape_quotes(s):
    # Escape backslashes first
    s = s.replace('\\', '\\\\')
    # Then escape quotes
    s = s.replace('"', '\\"')
    # Wrap in quotes
    return f'"{s}"'

# --------------------------------------------------------------

wipe()

print("example input:\n")
example_txt = get_raw(day=8, year=2015, file_name="example.txt")
example_txt = example_txt.strip().splitlines()
example_preview = example_txt
example_joined = "\n".join(example_preview)
print(example_joined,"\n")

example_code_lengths = [len(line) for line in example_preview]
example_total_code = sum(example_code_lengths)
print("code lengths:", example_code_lengths, example_total_code)  # [2, 5, 10, 6] 23

example_eval_lengths = [len(eval(line)) for line in example_preview]
example_total_eval = sum(example_eval_lengths)
print("eval lengths:", example_eval_lengths, example_total_eval)  # [0, 3, 7, 1]
example_overhead = example_total_code - example_total_eval
print("encoding overhead:", example_overhead)  # 23 - 11 = 12

part(1)

print("first 10 lines of input:\n")
input_txt = get_raw(day=8, year=2015)
input_txt = input_txt.strip().splitlines()
input_preview = input_txt[:10]
input_joined = "\n".join(input_preview)
print(input_joined, "\n")

preview_code_lengths = [len(line) for line in input_preview]
code_lengths = [len(line) for line in input_txt]
total_code = sum(code_lengths)
print(f"first 10 code lengths:\n{preview_code_lengths}\ntotal code: {total_code}\n")

preview_eval_lengths = [len(eval(line)) for line in input_preview]
input_eval_lengths = [len(eval(line)) for line in input_txt]
total_eval = sum(input_eval_lengths)
print(f"first 10 eval lengths:\n{preview_eval_lengths}\ntotal eval: {total_eval}\n")
input_overhead = total_code - total_eval
print("encoding overhead:", input_overhead, "\n")

part(2)

print("example escaped:\n")
example_escaped = [escape_quotes(line) for line in example_txt]
escaped_joined = "\n".join(example_escaped)
print(escaped_joined, "\n")

example_escaped_lengths = [len(line) for line in example_escaped]
example_total_escaped = sum(example_escaped_lengths)
example_escaped_overhead = example_total_escaped - example_total_code
print("escaped lengths:", example_escaped_lengths, example_total_escaped)  # [6, 9, 16, 11] 42
print("code lengths:", example_code_lengths, example_total_code)  # [2, 5, 10, 6] 23
print(f"escaped overhead: {example_total_escaped} - {example_total_code} = {example_escaped_overhead}")  # 42 - 23 = 19

print("\nfirst 10 lines of escaped input:\n")
input_escaped = [escape_quotes(line) for line in input_txt]
input_escaped_preview = input_escaped[:10]
input_escaped_joined = "\n".join(input_escaped_preview)
print(input_escaped_joined, "\n")

preview_escaped_lengths = [len(line) for line in input_escaped_preview]
input_escaped_lengths = [len(line) for line in input_escaped]
total_escaped = sum(input_escaped_lengths)
input_escaped_overhead = total_escaped - total_code
print(f"first 10 escaped lengths:\n{preview_escaped_lengths}\ntotal escaped: {total_escaped}\n") # 8356
print(f"first 10 code lengths:\n{preview_code_lengths}\ntotal code: {total_code}\n") # 6310
print(f"escaped overhead: {total_escaped} - {total_code} = {input_escaped_overhead}\n") # 2046
