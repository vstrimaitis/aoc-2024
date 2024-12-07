from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

Operator = tuple[str, Callable[[int, int], int]]

def is_solvable(lhs: int, rhs: list[int], operators: list[Operator]) -> bool:
    n = len(rhs)-1
    for ops in itt.product(operators, repeat=n):
        ans = rhs[0]
        for i in range(n):
            _, op_fn = ops[i]
            x = rhs[i+1]
            ans = op_fn(ans, x)
        if ans == lhs:
            return True
    return False

with PuzzleContext(year=2024, day=7) as ctx:
    ans1, ans2 = 0, 0

    add = ("+", lambda a, b: a+b)
    mul = ("*", lambda a, b: a*b)
    con = ("||", lambda a, b: int(str(a)+str(b)))

    lines = list(ctx.nonempty_lines)
    for i, l in enumerate(lines):
        print(f"{i+1}/{len(lines)}")
        [lhs, *rhs] = ints(l)
        if is_solvable(lhs, rhs, [add, mul]):
            ans1 += lhs
        if is_solvable(lhs, rhs, [add, mul, con]):
            ans2 += lhs

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
