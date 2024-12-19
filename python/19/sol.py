from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

PATTERNS = []

@ft.cache
def ways(s: str) -> int:
    if len(s) == 0:
        return 1
    ans = 0
    for p in PATTERNS:
        if s.startswith(p):
            ans += ways(s[len(p):])
    return ans
        

with PuzzleContext(year=2024, day=19) as ctx:
    a, b = ctx.groups
    PATTERNS = a.split(", ")
    
    ans1, ans2 = 0, 0
    for l in b.split():
        w = ways(l)
        if w > 0:
            ans1 += 1
        ans2 += w

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
