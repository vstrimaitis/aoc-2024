from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

def is_correct(xs):
    for i, a in enumerate(xs):
        for b in xs[i+1:]:
            if b in orders and a in orders[b]:
                return False
    return True

def reorder(xs):
    for i, a in enumerate(xs):
        for j, b in enumerate(xs[i+1:]):
            if b in orders and a in orders[b]:
                xs[i], xs[j] = xs[j], xs[i]

with PuzzleContext(year=2024, day=5) as ctx:
    ans1, ans2 = 0, 0

    a, b = ctx.groups
    orders = defaultdict(lambda: [])
    for l in a.split("\n"):
        x, y = ints(l)
        orders[x].append(y)

    for l in b.split("\n"):
        xs = ints(l)
        if is_correct(xs):
            ans1 += xs[len(xs)//2]
        else:
            reorder(xs)
            ans2 += xs[len(xs)//2]

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
