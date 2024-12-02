from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft


def is_safe(arr: list[int]):
    ds = diff_list(arr)

    same_sign = all(d > 0 for d in ds) or all(d < 0 for d in ds)
    small_diff = all(1 <= abs(d) <= 3 for d in ds)

    return same_sign and small_diff
    
def is_safe_2(arr: list[int]):
    for i in range(len(arr)):
        arr2 = arr[:i] + arr[i+1:]
        if is_safe(arr2):
            return True
    return False

with PuzzleContext(year=2024, day=2) as ctx:
    ans1, ans2 = None, None

    ans1 = 0
    ans2 = 0
    for l in ctx.nonempty_lines:
        arr = ints(l)
        if is_safe(arr):
            ans1 += 1
        if is_safe_2(arr):
            ans2 += 1

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
