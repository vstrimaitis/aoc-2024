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

def bfs(g: list[list[str]], start: Coord, ignore_walls: bool = False, max_dist: int = 10**100) -> dict[Coord, int]:
    q = deque()
    dists = {start: 0}
    q.append(start)
    while q:
        u = q.popleft()
        i, j = u
        if dists[u] > max_dist:
            continue
        for v in get_neigh_coords(g, i, j, DIRS_4):
            ii, jj = v
            if not ignore_walls and g[ii][jj] == "#":
                continue
            if v in dists:
                continue
            dists[v] = dists[u] + 1
            q.append((ii, jj))
    return {c: d for c, d in dists.items() if g[c[0]][c[1]] != "#"}

def get_cheats(g: list[list[str]], n: int, m: int) -> list[tuple[Coord, Coord, int]]:
    ans = []
    for i in range(n):
        print(f"{i+1}/{n}")
        for j in range(m):
            if g[i][j] == "#":
                continue
            dists = bfs(g, (i, j), ignore_walls=True, max_dist=20)
            for (ii, jj), d in dists.items():
                ans.append(((i, j), (ii, jj), d))
    return ans

with PuzzleContext(year=2024, day=20) as ctx:
    ans1, ans2 = None, None
    g, n, m =  to_grid(ctx.data)

    start = grid_find(g, "S")
    goal = grid_find(g, "E")

    d_from_start = bfs(g, start)
    d_to_end = bfs(g, goal)
    d = d_from_start[goal]
    all_cheats = get_cheats(g, n, m)


    limit = 100
    if ctx._is_running_on_sample():
        limit = 20
    ans1 = sum(
        1
        for u, v, c in all_cheats
        if c <= 2 and d - (d_from_start[u] + d_to_end[v] + c) >= limit
    )
    ctx.submit(1, str(ans1) if ans1 else None)

    if ctx._is_running_on_sample():
        limit = 50
    ans2 = sum(
        1
        for u, v, c in all_cheats
        if c <= 20 and d - (d_from_start[u] + d_to_end[v] + c) >= limit
    )
    ctx.submit(2, str(ans2) if ans2 else None)
