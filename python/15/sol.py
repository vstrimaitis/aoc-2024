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

def move_double(g: Grid, p1: Coord, p2: Coord, d: Dir, check_only: bool) -> tuple[Coord, Coord]:
    if lget(g, p1) != "[":
        nxt2, nxt1 = move_double(g, p2, p1, d, check_only)
        return nxt1, nxt2
    assert lget(g, p1) == "["
    assert lget(g, p2) == "]"

    i1, j1 = p1
    i2, j2 = p2
    di, dj = d
    nxt1 = i1+di, j1+dj
    nxt2 = i2+di, j2+dj
    
    def do_single_moves(check: bool):
        """Checks whether a move is possible and performs it if `check` is True"""
        if d == (0, -1):
            # going left - only need to check whether '[' can move
            if move(g, nxt1, d, check) != nxt1:
                return True
            return False
        elif d == (0, 1):
            # going right - only need to check whether ']' can move
            if move(g, nxt2, d, check) != nxt2:
                return True
            return False
        else:
            # going up or down - need to check if both can move
            if move(g, nxt1, d, check) != nxt1 and move(g, nxt2, d, check) != nxt2:
                return True
            return False
    # first, check if a move can be performed without actually doing it
    can_move = do_single_moves(True)
    if not can_move:
        return p1, p2
    # if everything is ok - perform the move
    do_single_moves(check_only)
    if not check_only:
        lset(g, p1, ".")
        lset(g, p2, ".")
        lset(g, nxt1, "[")
        lset(g, nxt2, "]")
    return nxt1, nxt2

def move(g: Grid, p: Coord, d: Dir, check_only: bool = False) -> Coord:
    i, j = p
    if g[i][j] == "#":
        return (i, j)
    di, dj = d
    ii, jj = i+di, j+dj
    if g[i][j] == ".":
        return (ii, jj)
    if g[i][j] in {"O", "@"}:
        nxt = move(g, (ii, jj), d, check_only)
        if nxt == (ii, jj):
            return p
        if not check_only:
            g[ii][jj] = g[i][j]
            g[i][j] = "."
        return ii, jj
    elif g[i][j] in {"[", "]"}:
        if g[i][j] == "[":
            return move_double(g, (i, j), (i, j+1), d, check_only)[0]
        else:
            return move_double(g, (i, j), (i, j-1), d, check_only)[0]
    assert False, "should never happen"

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