from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft


with PuzzleContext(year=2024, day=1) as ctx:
    ans1, ans2 = None, None

    L = []
    R = []
    for l in ctx.nonempty_lines:
        a, b = l.split("   ")
        L.append(int(a))
        R.append(int(b))
    L = sorted(L)
    R = sorted(R)

    ans1 = 0
    for a, b in zip(L, R):
        ans1 += abs(a-b)

    ctx.submit(1, str(ans1) if ans1 else None)

    ans2 = 0
    for x in L:
        ans2 += x * R.count(x)
    ctx.submit(2, str(ans2) if ans2 else None)
