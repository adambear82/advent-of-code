
# -------------------------------------------------------------

def parse(s):
    if not s:
        return [], [], []
    
    counts = []
    groups = []
    say = []
    
    run_char = s[0]
    run_len = 1
    
    for ch in s[1:]:
        if ch == run_char:
            run_len += 1
        else:
            # counts.append(run_len)
            # groups.append(int(run_char))
            say.append(run_len)
            say.append(int(run_char))
            run_char = ch
            run_len = 1
    
    # finalize last run
    # counts.append(run_len)
    # groups.append(int(run_char))
    say.append(run_len)
    say.append(int(run_char))
    flat_say = "".join(map(str, say))
    return flat_say

def run(s, n, note):
    print(f"\n{note}\n")
    s = str(s)
    for r in range(n):
        # print(f"run {r}: {s}") # comment out to hide intermediate steps
        s = parse(s)
    # print(f"run {r+1}: {s}\n") # comment out to hide final result
    print(f"length: {len(s)}\n")

# ------------------------------------------------------------

run(1, 5, "example:")

run(1113222113, 40, "part 1:")

run(1113222113, 50, "part 2:")
