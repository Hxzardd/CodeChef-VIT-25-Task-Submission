import os
import sys
from io import BytesIO, IOBase
from collections import defaultdict, deque, Counter
from itertools import permutations, combinations, product
from math import gcd, sqrt, ceil, floor, factorial
from heapq import heappush, heappop, heapify
from bisect import bisect_left, bisect_right, insort_left, insort_right
from functools import lru_cache, reduce

BUFSIZE = 8192

class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)

class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")

sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)

# Basic input functions for convenience
input = lambda: sys.stdin.readline().rstrip("\r\n")
readint = lambda: int(input())               # Read a single integer
readints = lambda: map(int, input().split())  # Read space-separated integers
readstr = lambda: input()                     # Read a single string
readstrs = lambda: input().split()            # Read space-separated strings
readarri = lambda: list(map(int, input().split()))  # Read array of integers
readarrs = lambda: input().split()                 # Read array of strings

def printarr(arr):
    sys.stdout.write(" ".join(map(str, arr)) + "\n")

def solve():
    pi = 355 / 113
    scrap_factor = 1 - (pi / 6)
    a, b, c = readints() # Read dimensions
    
    total_cubes = 0
    cuboid = [(a, b, c)] # Initialize with the full cuboid

    while cuboid:
        x, y, z = sorted(cuboid.pop(0)) # Sort dimensions (ensures we always take the biggest cube possible)
        
        if x == 0 or y == 0 or z == 0: # If any dimension is zero, skip
            continue
        
        max_cube_size = x # The largest cube that can be extracted
        num_cubes = (y // max_cube_size) * (z // max_cube_size) # Number of such cubes
        total_cubes += num_cubes # Update count

        if y % max_cube_size: # Add leftover cuboid sections for further cube processing
            cuboid.append((y % max_cube_size, max_cube_size, max_cube_size))
        if z % max_cube_size:
            cuboid.append((z % max_cube_size, y, max_cube_size))
    
    total_volume = a * b * c
    total_scrap = round(total_volume * scrap_factor)

    print(total_cubes)
    print(total_scrap)

if __name__ == "__main__":
    T = readint() # Read number of test cases
    for _ in range(T):
        solve() # Call the solve function for each test case
