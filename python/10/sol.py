from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft
from abc import ABC, abstractmethod

Coord = tuple[int, int]

T = TypeVar("T")


class Solver(ABC, Generic[T]):
    def __init__(self, s: str):
        self.g, self.n, self.m = to_grid(s)

    @abstractmethod
    def zero(self) -> T: ...

    @abstractmethod
    def one(self, c: Coord) -> T: ...

    @abstractmethod
    def combine(self, res1: T, res2: T) -> T: ...

    @abstractmethod
    def to_int(self, res: T) -> int: ...

    def solve(self) -> int:
        ans = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.g[i][j] == "0":
                    ans += self.to_int(self._dfs(i, j))
        return ans

    def _dfs(self, i: int, j: int) -> T:
        if self.g[i][j] == "9":
            return self.one((i, j))
        res = self.zero()
        for ii, jj in get_neigh_coords(self.g, i, j, DIRS_4):
            if int(self.g[ii][jj]) - int(self.g[i][j]) == 1:
                subres = self._dfs(ii, jj)
                res = self.combine(res, subres)
        return res


class ScoreSolver(Solver[set[Coord]]):
    def zero(self) -> set[Coord]:
        return set()

    def one(self, c: Coord) -> set[Coord]:
        return {c}

    def combine(self, res1: set[Coord], res2: set[Coord]) -> set[Coord]:
        return res1 | res2

    def to_int(self, res: set[Coord]) -> int:
        return len(res)


class RatingSolver(Solver[int]):
    def zero(self) -> int:
        return 0

    def one(self, c: Coord) -> int:
        return 1

    def combine(self, res1: int, res2: int) -> int:
        return res1 + res2

    def to_int(self, res: int) -> int:
        return res


with PuzzleContext(year=2024, day=10) as ctx:
    ans1 = ScoreSolver(ctx.data).solve()
    ctx.submit(1, str(ans1) if ans1 else None)

    ans2 = RatingSolver(ctx.data).solve()
    ctx.submit(2, str(ans2) if ans2 else None)
