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

def is_solvable_2(target: int, nums: list[int], operators: list[Operator]) -> bool:
    def gen(i: int, curr: int) -> bool:
        if i >= len(nums):
            return curr == target
        if curr > target:  # answers can only increase, so break early
            return False
        for _, op_fn in operators:
            if gen(i+1, op_fn(curr, nums[i])):
                return True
        return False
    return gen(0, 0)

with PuzzleContext(year=2024, day=7) as ctx:
    ans1, ans2 = 0, 0

    add = ("+", lambda a, b: a+b)
    mul = ("*", lambda a, b: a*b)
    con = ("||", lambda a, b: int(str(a)+str(b)))

    lines = list(ctx.nonempty_lines)
    for i, l in enumerate(lines):
        print(f"{i+1}/{len(lines)}")
        [lhs, *rhs] = ints(l)
        if is_solvable_2(lhs, rhs, [add, mul]):
            ans1 += lhs
        if is_solvable_2(lhs, rhs, [add, mul, con]):
            ans2 += lhs

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
