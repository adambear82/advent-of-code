
from utils.vibes import get_raw  # type: ignore

def parse_to_dict(text):
    graph = {}
    lines = text.strip().split("\n")
    for line in lines:
        if not line.strip():
            continue
        key, values = line.split(":")
        key = key.strip()
        value_list = values.strip().split()
        graph[key] = value_list
    return graph


def count_paths(graph, start, end, memo=None, visiting=None):
    """
    Count the number of distinct paths from `start` to `end`.
    Uses memoization and guards against cycles.
    """
    if memo is None:
        memo = {}
    if visiting is None:
        visiting = set()

    # Base cases
    if start == end:
        return 1
    if start not in graph or not graph[start]:
        return 0
    if start in memo:
        return memo[start]
    if start in visiting:
        # Cycle detected on current DFS branch; do not count this branch
        return 0

    visiting.add(start)
    total = 0
    for neighbor in graph[start]:
        total += count_paths(graph, neighbor, end, memo, visiting)
    visiting.remove(start)
    memo[start] = total
    return total


def _branch_connectors(idx, total):
    """
    Return a tuple (connector, next_prefix_piece) to render tree branches.
    ├── for mid branches, └── for last branch.
    """
    is_last = (idx == total - 1)
    connector = "└── " if is_last else "├── "
    next_prefix_piece = "    " if is_last else "│   "
    return connector, next_prefix_piece


def _leads_to_end(graph, node, end, memo=None):
    """
    Predicate: does `node` lead to `end` via any path?
    Uses memoization for efficiency. Safe against cycles.
    """
    if memo is None:
        memo = {}
    if node in memo:
        return memo[node]
    if node == end:
        memo[node] = True
        return True
    if node not in graph:
        memo[node] = False
        return False

    # To avoid cycles, we still rely on counting paths (which has cycle-guards)
    leads = count_paths(graph, node, end) > 0
    memo[node] = leads
    return leads


def print_tree(graph, start, end):
    """
    Print a hierarchical tree from `start` expanding only branches
    that eventually reach `end`. Uses Unicode box drawing.
    """
    # We precompute which nodes lead to `end` to prune dead branches.
    leads_memo = {}

    def dfs(node, prefix, seen):
        # Avoid reprinting cycles in the same visual branch
        if node in seen:
            print(prefix + "↺ " + node)  # indicate cycle visually
            return
        print(prefix + node)
        seen.add(node)

        # Collect children that lead to end
        children = graph.get(node, [])
        viable = [c for c in children if _leads_to_end(graph, c, end, leads_memo)]

        for i, child in enumerate(viable):
            connector, next_piece = _branch_connectors(i, len(viable))
            # For each child, print connector and recurse with updated prefix
            print(prefix + connector, end="")
            # We want child name to be printed on the same line, so dfs will print name without prefix duplication
            # Hack: pass an empty prefix for the child line; but continue with accumulated prefix afterwards
            # Better: have dfs print name directly; we already emitted connector.
            # So we adjust dfs to support "inline".
            # Simpler approach: call a child printer that prints child and recurses.
            _print_child(graph, child, end, prefix + next_piece, leads_memo, seen.copy())

    def _print_child(graph, node, end, prefix, leads_memo, seen):
        # Print the node name on same line (already had connector printed)
        print(node)
        # Then recurse for this child's children
        children = graph.get(node, [])
        viable = [c for c in children if _leads_to_end(graph, c, end, leads_memo)]

        if node in seen:
            # cycle marker
            print(prefix + "↺ " + node)
            return
        seen.add(node)

        for i, child in enumerate(viable):
            connector, next_piece = _branch_connectors(i, len(viable))
            print(prefix + connector, end="")
            _print_child(graph, child, end, prefix + next_piece, leads_memo, seen.copy())

    dfs(start, prefix="", seen=set())


# --------------------------
# Example usage
# --------------------------
url_text = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

url_text = get_raw(11)

graph_dict = parse_to_dict(url_text)

# Print the hierarchical tree from "you" to "out"
print_tree(graph_dict, "you", "out")

# Count paths and print the total
total = count_paths(graph_dict, "you", "out")
print(f'\nTotal paths from you to out: {total}')
