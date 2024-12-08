from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft


def calc(n: int, m: int, c1: CCoord, c2: CCoord, mults: list[int] | None) -> set[CCoord]:
    res: set[CCoord] = set()
    d = c2 - c1
    if mults is None:
        curr = c1
        while is_within_bounds(curr, n, m):
            res.add(curr)
            curr += d
        curr = c1
        while is_within_bounds(curr, n, m):
            res.add(curr)
            curr -= d
    else:
        for mult in mults:
            res.add(c1 + mult * d)
    return {c for c in res if is_within_bounds(c, n, m)}


with PuzzleContext(year=2024, day=8) as ctx:
    g, n, m = to_grid(ctx.data)
    g = to_inf_grid(g)
    poss: dict[str, list[CCoord]] = defaultdict(lambda: [])
    for c, val in g.items():
        if val != ".":
            poss[val].append(c)

    pairs = [
        (a1, a2)
        for antennas in poss.values()
        for a1 in antennas
        for a2 in antennas
        if a1 != a2
    ]

    ans1 = len(
        ft.reduce(
            lambda acc, s: acc | s,
            [
                calc(n, m, a1, a2, mults=[-1, 2])
                for a1, a2 in pairs
            ],
            set(),
        )
    )
    ctx.submit(1, str(ans1) if ans1 else None)

    ans2 = len(
        ft.reduce(
            lambda acc, s: acc | s,
            [
                calc(n, m, a1, a2, mults=None)
                for a1, a2 in pairs
            ],
            set(),
        )
    )
    ctx.submit(2, str(ans2) if ans2 else None)
