from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

State = tuple[complex, complex]
Grid = dict[complex, str]

def out_of_bounds(coord: complex, n: int, m: int) -> bool:
    i, j = to_coord(coord)
    return not (0 <= i < n and 0 <= j < m)

def get_next(state: State, g: Grid) -> State:
    coord, d = state
    while True:
        nxt = coord + d
        if g.get(nxt) != "#":
            return nxt, d
        d = rot_cw(d)


def to_dir(c: str) -> complex:
    return {
        "^": -1,
        ">": 1j,
        "v": 1,
        "<": -1j,
    }[c]

def solve(g: Grid, n: int, m: int) -> tuple[bool, set[complex]]:
    curr = [
        (coord, to_dir(val))
        for coord, val in g.items()
        if val in "><^v"
    ][0]

    seen = {curr}
    while True:
        curr = get_next(curr, g)
        if out_of_bounds(curr[0], n, m):
            break
        if curr in seen:
            return True, set()
        seen.add(curr)
    return False, {coord for (coord, _) in seen}

with PuzzleContext(year=2024, day=6) as ctx:
    g, n, m = to_grid(ctx.data)
    g = to_inf_grid(g)

    _, visited = solve(g, n, m)
    ans1 = len(visited)
    ctx.submit(1, str(ans1) if ans1 else None)

    ans2 = 0
    for coord in visited:
        if g[coord] == ".":
            g[coord] = "#"
            is_stuck, _ = solve(g, n, m)
            if is_stuck:
                ans2 += 1
            g[coord] = "."
    ctx.submit(2, str(ans2) if ans2 else None)
