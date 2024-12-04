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
    ans1 = sum(
        [
            "XMAS"
            == "".join(
                g[ii][jj]
                for d in range(4)
                if 0 <= (ii := i + di * d) < n and 0 <= (jj := j + dj * d) < m
            )
            for i in range(n)
            for j in range(m)
            for di, dj in DIRS_8
        ]
    )

    ctx.submit(1, str(ans1) if ans1 else None)

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if g[i][j] == "A":
                a = g[i - 1][j - 1] + g[i + 1][j + 1]
                b = g[i - 1][j + 1] + g[i + 1][j - 1]
                exp = {"MS", "SM"}
                if a in exp and b in exp:
                    ans2 += 1
    ctx.submit(2, str(ans2) if ans2 else None)
