from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

@ft.cache
def cnt(x, n) -> int:
    if n == 0:
        return 1
    if x == 0:
        return cnt(1, n-1)
    s = str(x)
    if len(s) % 2 == 0:
        a = int(s[:len(s)//2])  
        b = int(s[len(s)//2:])
        return cnt(a, n-1) + cnt(b, n-1)
    return cnt(x*2024, n-1)

with PuzzleContext(year=2024, day=11) as ctx:
    ans1, ans2 = 0, 0

    arr = ints(ctx.data)
    for x in arr:
        ans1 += cnt(x, 25)
        ans2 += cnt(x, 75)
    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
