from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

def solve(xa: int, ya: int, xb: int, yb: int, x: int, y: int) -> tuple[int, int] | None:
    A = xa*y-x*ya
    B = xa*yb-xb*ya
    if A % B != 0:
        return None
    b = A // B
    C = x - b*xb
    D = xa
    if C % D != 0:
        return None
    a = C//D
    if a >= 0 and b >= 0:
        return (a, b)
    return None

with PuzzleContext(year=2024, day=13) as ctx:
    ans1, ans2 = 0, 0
    delta = 10000000000000
    for g in ctx.groups:
        xa, ya, xb, yb, x, y = ints(g)
        
        s = solve(xa, ya, xb, yb, x, y)
        if s is not None:
            a, b = s
            ans1 += 3*a+b
        
        s = solve(xa, ya, xb, yb, x+delta, y+delta)
        if s is not None:
            a, b = s
            ans2 += 3*a+b

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
