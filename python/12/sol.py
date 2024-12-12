from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

Coord = tuple[int, int]

DIRS_CORNERS = []
for k, (di1, dj1) in enumerate(DIRS_4):
    for di2, dj2 in DIRS_4[k+1:]:
        if di1 != di2 and dj1 != dj2:
            DIRS_CORNERS.append((
                (di1, dj1),
                (di2, dj2),
                (di1+di2, dj1+dj2),
            ))

def dfs(g: list[list[str]], i: int, j: int, visited: set[Coord]):
    visited.add((i, j))
    for ii, jj in get_neigh_coords(g, i, j, DIRS_4):
        if g[ii][jj] == g[i][j] and (ii, jj) not in visited:
            dfs(g, ii, jj, visited)

def get(g: list[list[str]], coord: Coord) -> str | None:
    i, j = coord
    n = len(g)
    m = len(g[0])
    if 0 <= i < n and 0 <= j < m:
        return g[i][j]
    return None

def calc1(group: set[Coord]) -> int:
    area = len(group)
    perimeter = 0
    for i, j in group:
        for di, dj in DIRS_4:
            ii = i + di
            jj = j + dj
            if (ii, jj) not in group:
                perimeter += 1
    return area * perimeter

def calc2(group: set[Coord]) -> int:
    area = len(group)
    n_sides = 0

    for i, j in group:
        for (a_di, a_dj), (b_di, b_dj), (c_di, c_dj) in DIRS_CORNERS:
            side1 = (i+a_di, j+a_dj)
            side2 = (i+b_di, j+b_dj)
            corner = (i+c_di, j+c_dj)
            x = get(g, side1)
            y = get(g, side2)
            z = get(g, corner)
            if x == g[i][j] and y == g[i][j]:
                if z != g[i][j]:
                    # "inner" corner
                    n_sides += 1
            elif x != g[i][j] and y != g[i][j]:
                # "outer" corner
                n_sides += 1
        

    return area * n_sides

with PuzzleContext(year=2024, day=12) as ctx:
    ans1, ans2 = None, None

    g, n, m = to_grid(ctx.data)
    groups = []
    visited = set()
    for i in range(n):
        for j in range(m):
            if (i, j) not in visited:
                group = set()
                dfs(g, i, j, group)
                groups.append(group)
                visited |= group
                
    ans1 = sum(calc1(group) for group in groups)
    ctx.submit(1, str(ans1) if ans1 else None)

    ans2 = sum(calc2(group) for group in groups)
    ctx.submit(2, str(ans2) if ans2 else None)
