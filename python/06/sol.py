from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

def rot(d):
    dirs = "^>v<"
    i = dirs.index(d)
    return dirs[(i+1)%len(dirs)]

def move(i, j, d):
    return {
        ">": (i, j+1),
        "<": (i, j-1),
        "v": (i+1, j),
        "^": (i-1, j),
    }[d]

def out_of_bounds(i, j, n, m):
    return not (0 <= i < n and 0 <= j < m)

def get_next(state, g, n, m):
    i, j, d = state
    while True:
        ii, jj = move(i, j, d)
        if out_of_bounds(ii, jj, n, m):
            return (ii, jj, None)
        if g[ii][jj] != "#":
            return (ii, jj, d)
        d = rot(d)


def solve(g, n, m):
    curr = None
    for i in range(n):
        for j in range(m):
            if g[i][j] in "><^v":
                curr = (i, j, g[i][j])
    assert curr is not None

    seen = set()
    while True:
        curr = get_next(curr, g, n, m)
        if curr[-1] is None: # escaped
            break
        if curr in seen:
            return True, None
        seen.add(curr)
    return False, {(i, j) for (i, j, _) in seen}

with PuzzleContext(year=2024, day=6) as ctx:
    g, n, m = to_grid(ctx.data)

    _, visited = solve(g, n, m)
    assert visited is not None
    ans1 = len(visited)
    ctx.submit(1, str(ans1) if ans1 else None)

    ans2 = 0
    for i, j in visited:
        if g[i][j] == ".":
            g[i][j] = "#"
            is_stuck, _ = solve(g, n, m)
            if is_stuck:
                ans2 += 1
            g[i][j] = "."
    ctx.submit(2, str(ans2) if ans2 else None)
