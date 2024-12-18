from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

class DSU:
    def __init__(self, n: int):
        self.n = n
        self.size = [1 for _ in range(n)]
        self.parent = [i for i in range(n)]
    
    def find(self, x: int) -> int:
        if self.parent[x] == x:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def same(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def unite(self, x: int, y: int) -> None:
        if self.same(x, y):
            return
        x = self.find(x)
        y = self.find(y)
        if self.size[x] > self.size[y]:
            x, y = y, x
        self.size[y] += self.size[x]
        self.parent[x] = y

class DSU2:
    def __init__(self, n: int, m: int):
        self._dsu = DSU(n*m)
        self.n = n
        self.m = m
    
    def find(self, p: tuple[int, int]) -> tuple[int, int]:
        id = self._to_id(p)
        id = self._dsu.find(id)
        return self._from_id(id)
    
    def unite(self, a: tuple[int, int], b: tuple[int, int]) -> None:
        if self._is_within_bounds(a) and self._is_within_bounds(b):
            id_a = self._to_id(a)
            id_b = self._to_id(b)
            self._dsu.unite(id_a, id_b)

    def same(self, a: tuple[int, int], b: tuple[int, int]) -> bool:
        id_a = self._to_id(a)
        id_b = self._to_id(b)
        return self._dsu.same(id_a, id_b)
    
    def _to_id(self, p: tuple[int, int]) -> int:
        i, j = p
        return i*self.m + j

    def _from_id(self, id: int) -> tuple[int, int]:
        i = id // self.m
        j = id % self.m
        return i, j
    
    def _is_within_bounds(self, p: tuple[int, int]) -> bool:
        i, j = p
        return 0 <= i < self.n and 0 <= j < self.m

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

    g = build_grid(n, m, walls)
    dsu = DSU2(n, m)
    for i in range(n):
        for j in range(m):
            if g[i][j] != ".":
                continue
            for ii, jj in get_neigh_coords(g, i, j, DIRS_4):
                if g[ii][jj] == ".":
                    dsu.unite((i, j), (ii, jj))
    ans2 = walls[-1]
    for y, x in reversed(walls):
        for dy, dx in DIRS_4:
            dsu.unite((y, x), (y+dy, x+dx))
        ans2 = y, x
        if dsu.same(start, goal):
            break
    ans2 = ",".join(map(str, reversed(ans2)))

    ctx.submit(2, str(ans2) if ans2 else None)
