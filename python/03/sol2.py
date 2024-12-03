from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft



with PuzzleContext(year=2024, day=3) as ctx:
    ans1 = 0
    for x in re.findall(r"mul\((\d+),(\d+)\)", ctx.data):
        ans1 += int(x[0]) * int(x[1])
    
    ans2 = 0
    patterns = {
        "do": (
            r"do\(\)",
            lambda x, _: (True, x[1]),
        ),
        "dont": (
            r"don't\(\)",
            lambda x, _: (False, x[1]),
        ),
        "mul": (
            r"mul\((\d+),(\d+)\)",
            lambda x, m: (False, x[1]) if not x[0] else (True, x[1] + int(m[1])*int(m[2])),
        ),
    }
    pattern = "|".join(f"(?P<{name}>{p})" for name, (p, _) in patterns.items())
    state = (True, 0) # (is_active, ans)
    for m in re.finditer(pattern, ctx.data):
        for k, (_, f) in patterns.items():
            if m.group(k) is not None:
                state = f(state, [g for g in m.groups() if g is not None])
                break
                
    ans2 = state[1]

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
