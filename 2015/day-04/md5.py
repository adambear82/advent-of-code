# generated using antigravity
# MD5 is a hash function that takes an input (or 'message') and returns
# a fixed-size string of bytes, known as the 'digest'.
# In this case, we're using it to find the smallest positive integer i
# such that the MD5 hash of the string "ckczppom" + i starts with 5 or 6 zeroes.
# The first such integer is the answer to the puzzle.
# The hashlib module provides a simple interface to many secure hash and message digest algorithms.
# hashlib.md5() returns a new hash object that can be used to compute the MD5 hash of a string.
# The encode() method is used to convert the string to bytes, which is required by the hashlib module.
# The hexdigest() method returns the hash value as a lowercase hex string.


import hashlib

def solve():
    secret_key = "ckczppom"
    i = 1
    part1_found = False
    part2_found = False
    
    while not (part1_found and part2_found):
        candidate = f"{secret_key}{i}"
        hash_result = hashlib.md5(candidate.encode()).hexdigest()
        
        if not part1_found and hash_result.startswith("00000"):
            print(f"Part 1 Answer (5 zeroes): {i}")
            print(f"Hash: {hash_result}")
            part1_found = True
            
        if not part2_found and hash_result.startswith("000000"):
            print(f"Part 2 Answer (6 zeroes): {i}")
            print(f"Hash: {hash_result}")
            part2_found = True
            
        i += 1

if __name__ == "__main__":
    solve()
