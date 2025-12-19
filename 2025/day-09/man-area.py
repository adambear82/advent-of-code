from utils.vibes import get_raw  # type: ignore

url_text = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

# url_text = get_raw(9)

rows = url_text.strip().splitlines()

pairs = []
for line in rows:
    a_str, b_str = line.split(',')   # split on comma
    pairs.append([int(a_str), int(b_str)])  # convert to ints

print(f"List of coordinate pairs:\n{pairs}\n")

rects = []
for i, (x1, y1) in enumerate(pairs): # enum
    
    print(f"\nPair {i}: x1={x1}, y1={y1}")
    for j in range(len(pairs)):
        if i == j: # not interested in zero area rectangles
            continue
        x2, y2 = pairs[j]
        manhattan_area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        print(f"  to Pair {j}: x2={x2}, dy2={y2} => Manhattan area = {manhattan_area}")
        #print(f"[{i}][{j}], area: <{manhattan_area}>")
        rects.append(["\narea", manhattan_area,
                      "\n [i]", i,
                      "\n [j]", j,
                      "\n  x1", x1,
                      "\n  x2", x2,
                      "\n  y1", y1,
                      "\n  y2", y2])
        rects.sort(key=lambda x: x[1], reverse=True)
        rects = rects[:1]  # keep only largest

rects = [item for sublist in rects for item in sublist] # flatten list

formatted = ", ".join(str(item) for item in rects) # make a single string

# part 1 
print(f"\nlargest rectangle area:\n{formatted}\n")

print(pairs)

trans_tuples = zip(*pairs)  # <zip object at ...>
trans_list = [list(row) for row in trans_tuples]
x_list, y_list = trans_list
x_min = min(x_list)
x_max = max(x_list)
y_min = min(y_list)
y_max = max(y_list)
width = x_max - x_min + 1
height = y_max -y_min + 1


lines = []
for _ in range(height): # "_" to indicate we dont care about variable
    lines.append("." * width)

result = "\n".join(lines)

print(width, height)
print(result)
print(lines)
