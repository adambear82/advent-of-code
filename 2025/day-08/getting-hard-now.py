from utils.vibes import get_raw  # type: ignore

from typing import List, Tuple

class DSU:
    """Disjoint Set Union (Union-Find) with path compression and union by size."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def parse_points(text: str) -> List[Tuple[int, int, int]]:
    """
    Parse puzzle input of lines 'X,Y,Z' into a list of (x, y, z) tuples.
    """
    points: List[Tuple[int, int, int]] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        x, y, z = map(int, s.split(","))
        points.append((x, y, z))
    return points


def product_of_top_three_after_k_attempts(
    points: List[Tuple[int, int, int]],
    k: int
) -> Tuple[int, List[int]]:
    """
    Consider edges in ascending squared distance and make exactly k attempts:
      - For each of the k shortest edges, if endpoints are in different components, union them.
      - If they're already connected, it's a no-op, but still counts as an attempt.
    Returns (product of the top 3 component sizes, sizes_desc).
    """
    n = len(points)
    if n == 0:
        return 1, []

    # Build all pairwise squared distances
    edges = []
    for i in range(n):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            d2 = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
            edges.append((d2, i, j))
    edges.sort(key=lambda e: e[0])

    dsu = DSU(n)
    attempts = 0
    idx = 0
    while attempts < k and idx < len(edges):
        _, i, j = edges[idx]
        # Attempt: union iff in different components; else no-op
        if dsu.find(i) != dsu.find(j):
            dsu.union(i, j)
        attempts += 1
        idx += 1

    # Count component sizes
    comp_count = {}
    for i in range(n):
        r = dsu.find(i)
        comp_count[r] = comp_count.get(r, 0) + 1
    sizes = sorted(comp_count.values(), reverse=True)

    # Product of top 3 (pad if fewer than 3)
    top = sizes[:3] + [1] * max(0, 3 - len(sizes))
    product = top[0] * top[1] * top[2]
    return product, sizes



url_text = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

url_text = get_raw(8)

points = parse_points(url_text)
product, sizes_desc = product_of_top_three_after_k_attempts(points, k=1000)

workings = str(sizes_desc[0]) + " * " + str(sizes_desc[1]) + " * " + str(sizes_desc[2])

print(f"\npart 1:\n\nsizes_desc: {sizes_desc[0:5]} ....truncated\n")     # -> [5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1]

print(f"top three: {workings} = {product}\n")        # -> 40

