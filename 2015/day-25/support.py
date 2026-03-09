MOD = 33554393
A = 252533
START = 20151125

def index_for(r, c):
    """1-based index n for position (r, c) in the diagonal ordering."""
    k = r + c - 2
    T = k * (k + 1) // 2
    return T + c  # n

def code_at(r, c, start=START, a=A, mod=MOD):
    """Compute the code at (row r, col c) directly, no grids needed."""
    n = index_for(r, c)
    # START * (A ** (n-1)) % MOD
    return (start * pow(a, n - 1, mod)) % mod

print(code_at(2981, 3075))
