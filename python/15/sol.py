from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft
from copy import deepcopy

Grid = list[list[str]]
Coord = tuple[int, int]
Dir = tuple[int, int]

def can_move(g: Grid, p: Coord, d: Dir) -> bool:
    i, j = p
    if g[i][j] == "#":
        return False
    if g[i][j] == ".":
        return True
    di, dj = d
    ii = i+di
    jj = j+dj
    if g[i][j] in {"O", "@"}:
        return can_move(g, (ii, jj), d)
    if g[i][j] in {"[", "]"}:
        if g[i][j] == "[":
            pair_coord = (i, j+1)
            assert lget(g, pair_coord) == "]"
        else:
            pair_coord = (i, j-1)
            assert lget(g, pair_coord) == "["
        
        if (ii, jj) == pair_coord:
            to_check = [(ii+di, jj+dj)]
        elif di == 0:
            to_check = [(ii, jj)]
        else:
            to_check = [(ii, jj), (pair_coord[0]+di, pair_coord[1]+dj)]

        for pp in to_check:
            if not can_move(g, pp, d):
                return False
        return True
    assert False


def move_double(g: Grid, p1: Coord, p2: Coord, d: Dir) -> tuple[Coord, Coord]:
    if lget(g, p1) != "[":
        nxt2, nxt1 = move_double(g, p2, p1, d)
        return nxt1, nxt2
    assert lget(g, p1) == "["
    assert lget(g, p2) == "]"

    i1, j1 = p1
    i2, j2 = p2
    di, dj = d
    nxt1 = i1+di, j1+dj
    nxt2 = i2+di, j2+dj
    
    if d == (0, -1):
        move(g, nxt1, d)
    elif d == (0, 1):
        move(g, nxt2, d)
    else:
        move(g, nxt1, d)
        move(g, nxt2, d)
    lset(g, p1, ".")
    lset(g, p2, ".")
    lset(g, nxt1, "[")
    lset(g, nxt2, "]")
    return nxt1, nxt2

def move(g: Grid, p: Coord, d: Dir) -> Coord:
    if not can_move(g, p, d):
        return p
    i, j = p
    di, dj = d
    ii = i+di
    jj = j+dj
    if g[i][j] == ".":
        return (ii, jj)
    if g[i][j] in {"O", "@"}:
        move(g, (ii, jj), d)
        g[ii][jj] = g[i][j]
        g[i][j] = "."
        return ii, jj
    elif g[i][j] in {"[", "]"}:
        if g[i][j] == "[":
            return move_double(g, (i, j), (i, j+1), d)[0]
        else:
            return move_double(g, (i, j), (i, j-1), d)[0]
    return (i, j)

def parse_dir(s: str) -> Dir:
    return {
        ">": (0, 1),
        "<": (0, -1),
        "^": (-1, 0),
        "v": (1, 0),
    }[s]

def parse(ctx: PuzzleContext) -> tuple[Grid, tuple[int, int], list[Dir]]:
    a, b = ctx.groups
    instructions = [
        parse_dir(c) for c in b.replace("\n", "")
    ]
    g, n, m = to_grid(a)
    start = [
        (i, j)
        for i in range(n)
        for j in range(m)
        if g[i][j] == "@"
    ][0]
    return g, start, instructions

def solve(g: Grid, start: Coord, dirs: list[Dir]) -> int:
    g = deepcopy(g)
    curr = start
    for d in dirs:
        curr = move(g, curr, d)

    ans = 0
    for i, r in enumerate(g):
        for j, c in enumerate(r):
            if c in ["O", "["]:
                ans += 100*i + j
    return ans

def expand(s: str) -> str:
    return {
        "#": "##",
        "O": "[]",
        ".": "..",
        "@": "@.",
    }[s]

with PuzzleContext(year=2024, day=15) as ctx:
    g, start, dirs = parse(ctx)
    
    ans1 = solve(g, start, dirs)
    ctx.submit(1, str(ans1))

    g = [
        [
            cc
            for c in r
            for cc in list(expand(c))
        ]
        for r in g
    ]
    start = (start[0], start[1] * 2)
    ans2 = solve(g, start, dirs)
    ctx.submit(2, str(ans2))