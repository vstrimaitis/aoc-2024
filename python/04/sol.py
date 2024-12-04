from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

with PuzzleContext(year=2024, day=4) as ctx:
    ans1, ans2 = 0, 0

    g, n, m = to_grid(ctx.data)
    for i in range(n):
        for j in range(m):
            if g[i][j] == "X":
                for di, dj in DIRS_8:
                    ii, jj = i, j
                    found = True
                    for c in "XMAS":
                        if not (0 <= ii < n and 0 <= jj < m and g[ii][jj] == c):
                            found = False
                            break
                        ii += di
                        jj += dj
                    if found:
                        ans1 += 1

    ctx.submit(1, str(ans1) if ans1 else None)


    for i in range(1, n-1):
        for j in range(1, m-1):
            if g[i][j] == "A":
                a = g[i-1][j-1]+g[i+1][j+1]
                b = g[i-1][j+1]+g[i+1][j-1]
                exp = {"MS", "SM"}
                if a in exp and b in exp:
                    ans2 += 1
    ctx.submit(2, str(ans2) if ans2 else None)
