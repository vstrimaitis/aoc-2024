from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft
from enum import Enum, auto

Coord = tuple[int, int]

def dfs(g: list[list[str]], u: Coord, dists: dict[Coord, int]) -> None:
    i, j = u
    assert g[i][j] != "#"
    for v in get_neigh_coords(g, i, j, DIRS_4):
        ii, jj = v
        if g[ii][jj] != "#" and v not in dists:
            dists[v] = dists[u] + 1
            dfs(g, v, dists)

def get_square(g: list[list[str]], i: int, j: int, size: int):
    for di in range(-size, size+1):
        for dj in range(-size, size+1):
            d = abs(di) + abs(dj)
            if d > size:
                continue
            ii = i + di
            jj = j + dj
            if 0 <= ii < n and 0 <= jj < m and g[ii][jj] != "#":
                yield ii, jj, d

def solve(g: list[list[str]], n: int, m: int, dists_from_start: dict[Coord, int], full_dist: int, max_cheat_size: int, min_gains: int) -> int:
    ans = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] == "#":
                continue
            for ii, jj, c in get_square(g, i, j, max_cheat_size):
                d1 = dists_from_start[(i, j)]
                d2 = full_dist - dists_from_start[(ii, jj)]
                d = d1 + d2 + c
                if full_dist-d >= min_gains:
                    ans += 1
    return ans


with PuzzleContext(year=2024, day=20) as ctx:
    g, n, m =  to_grid(ctx.data)
    start = grid_find(g, "S")
    goal = grid_find(g, "E")

    dists = {start: 0}
    dfs(g, start, dists)
    full_dist = dists[goal]

    ans1 = solve(
        g, n, m, dists, full_dist,
        max_cheat_size=2, min_gains=20 if ctx._is_running_on_sample() else 100,
    )
    ctx.submit(1, str(ans1) if ans1 else None)

    ans2 = solve(
        g, n, m, dists, full_dist,
        max_cheat_size=20, min_gains=50 if ctx._is_running_on_sample() else 100,
    )
    ctx.submit(2, str(ans2) if ans2 else None)
