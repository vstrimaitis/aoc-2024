from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

def bfs(g, start, goal):
    q = deque()
    dists = dict()
    dists[start] = 0
    q.append(start)
    while q:
        u = q.popleft()
        if u == goal:
            return dists[u]
        for v in get_neigh_coords(g, u[0], u[1], DIRS_4):
            if lget(g, v) == "#":
                continue
            if v in dists:
                continue
            dists[v] = dists[u] + 1
            q.append(v)
    return -1

def build_grid(n, m, walls):
    walls = set(walls)
    return [
        ["." if (i, j) not in walls else "#" for j in range(m)]
        for i in range(n)
    ]

with PuzzleContext(year=2024, day=18) as ctx:
    walls = []
    for l in ctx.nonempty_lines:
        x, y = ints(l)
        walls.append((y, x))
    
    n, m = 71, 71
    limit = 1024
    if ctx._is_running_on_sample():
        n, m = 7, 7
        limit = 12

    start = (0, 0)
    goal = (n-1, m-1)
    ans1 = bfs(build_grid(n, m, walls[:limit]), start, goal)
    ctx.submit(1, str(ans1) if ans1 else None)

    lo = 0
    hi = len(walls)-1
    while lo < hi:
        mid = (lo + hi) // 2
        d = bfs(build_grid(n, m, walls[:mid+1]), start, goal)
        if d == -1:
            hi = mid
        else:
            lo = mid+1

    y, x = walls[lo]
    ans2 = f"{x},{y}"
    ctx.submit(2, str(ans2) if ans2 else None)
