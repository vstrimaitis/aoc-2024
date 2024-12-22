from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft


def prune(x):
    return x % 16777216

def mix(x, y):
    return x ^ y

def nxt(x):
    x = prune(mix(x*64, x))
    x = prune(mix(x//32, x))
    x = prune(mix(x*2048, x))
    return x

def get_seq(x, n=2000):
    arr = []
    for _ in range(n):
        x = nxt(x)
        arr.append(x)
    return arr

with PuzzleContext(year=2024, day=22) as ctx:
    sequences = [get_seq(int(l)) for l in ctx.nonempty_lines]
    ans1 = sum(s[-1] for s in sequences)
    ctx.submit(1, str(ans1) if ans1 else None)

    totals = defaultdict(lambda: 0)
    for seq in sequences:
        prices = [x%10 for x in seq]
        seen = set()
        for price, needle in zip(prices[4:], windows(diff_list(prices), 4)):
            t = tuple(needle)
            if t not in seen:
                totals[t] += price
            seen.add(t)
    ans2 = max(totals.values())
    ctx.submit(2, str(ans2) if ans2 else None)
