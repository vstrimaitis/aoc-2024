from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

def parse():
    rules, updates = ctx.groups

    constraints = set()
    for l in rules.split("\n"):
        a, b = tuple(ints(l))
        constraints.add((a, b))

    return constraints, [ints(l) for l in updates.split("\n")]



with PuzzleContext(year=2024, day=5) as ctx:
    ans1, ans2 = 0, 0

    constraints, updates = parse()

    for xs in updates:
        in_order = True
        for i in range(len(xs)):
            for j in range(i+1, len(xs)):
                if (xs[j], xs[i]) in constraints:
                    in_order = False
                    xs[i], xs[j] = xs[j], xs[i]
        if in_order:
            ans1 += xs[len(xs)//2]
        else:
            ans2 += xs[len(xs)//2]

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
