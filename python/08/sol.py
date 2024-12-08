from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft


def calc(n: int, m: int, ants: list[CCoord], mults: list[int] | None) -> set[CCoord]:
    res: set[CCoord] = set()
    for c1 in ants:
        for c2 in ants:
            if c1 == c2:
                continue
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

    ans1 = len(
        ft.reduce(
            lambda acc, s: acc | s,
            [calc(n, m, antennas, mults=[-1, 2]) for antennas in poss.values()],
            set(),
        )
    )
    ctx.submit(1, str(ans1) if ans1 else None)

    ans2 = len(
        ft.reduce(
            lambda acc, s: acc | s,
            [calc(n, m, antennas, mults=None) for antennas in poss.values()],
            set(),
        )
    )
    ctx.submit(2, str(ans2) if ans2 else None)
