from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

def calc(s: str) -> int:
    ans = 0
    for x in re.findall(r"mul\((\d+),(\d+)\)", s):
        ans += int(x[0]) * int(x[1])
    return ans


with PuzzleContext(year=2024, day=3) as ctx:
    ans1 = calc(ctx.data)
    
    s = (
        ("do()" + ctx.data)
        .replace("\n", "")
        .replace("do()", "\ndo()")
        .replace("don't()", "\ndon't()")
    )
    ans2 = 0
    for l in s.split("\n"):
        if l.startswith("do()"):
            ans2 += calc(l)

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
