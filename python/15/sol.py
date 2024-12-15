from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

def can_move(g, n, m, p, d, ign=False):
    i, j = p
    di, dj = d
    ii = i+di
    jj = j+dj
    if g[i][j] == "#":
        return False
    if g[i][j] == ".":
        return True
    if g[i][j] in {".", "O", "@"}:
        return can_move(g, n, m, (ii, jj), d)
    if g[i][j] == "[":
        assert g[i][j+1] == "]"
        if d == (0, 1):
            return can_move(g, n, m, (ii, jj), d, ign=True)
        if d == (0, -1):
            return can_move(g, n, m, (ii, jj), d)
        if ign:
            return can_move(g, n, m, (ii, jj), d)
        else:
            return can_move(g, n, m, (ii, jj), d, ign) and can_move(g, n, m, (ii, jj+1), d, ign)
    if g[i][j] == "]":
        assert g[i][j-1] == "["
        if d == (0, -1):
            return can_move(g, n, m, (ii, jj), d, ign=True)
        if d == (0, 1):
            return can_move(g, n, m, (ii, jj), d)
        if ign:
            return can_move(g, n, m, (ii, jj), d)
        else:
            return can_move(g, n, m, (ii, jj), d, ign) and can_move(g, n, m, (ii, jj-1), d, ign)
    assert False


def move(g, n, m, p, d, ign=False):
    i, j = p
    di, dj = d
    ii = i+di
    jj = j+dj
    if g[i][j] == "#":
        return (i, j)
    if g[i][j] == ".":
        return (ii, jj)
    if g[i][j] in {".", "O", "@"}:
        if can_move(g, n, m, (ii, jj), d):
            move(g, n, m, (ii, jj), d)
            g[ii][jj] = g[i][j]
            g[i][j] = "."
            return ii, jj
        return i, j
    elif g[i][j] in {"[", "]"}:
        if g[i][j] == "[":
            assert g[i][j+1] == "]"
            if (ii, jj) == (i, j+1):
                if can_move(g, n, m, (i, j+1), d):
                    move(g, n, m, (i, j+1), d, ign=True)
                    g[i][j+1] = g[i][j]
                    g[i][j] = "."
                    return ii, jj
                return i, j
            if ign:
                if can_move(g, n, m, (ii, jj), d):
                    move(g, n, m, (ii, jj), d)
                    g[ii][jj] = g[i][j]
                    g[i][j] = "."
                    return ii, jj
                return i, j
            else:
                if can_move(g, n, m, (ii, jj), d) and can_move(g, n, m, (ii, jj+1), d):
                    move(g, n, m, (ii, jj), d)
                    move(g, n, m, (ii, jj+1), d)
                    g[ii][jj] = g[i][j]
                    g[ii][jj+1] = g[i][j+1]
                    g[i][j] = "."
                    g[i][j+1] = "."
                    return ii, jj
                return i, j
        if g[i][j] == "]":
            assert g[i][j-1] == "["
            if (ii, jj) == (i, j-1):
                if can_move(g, n, m, (ii, jj), d):
                    move(g, n, m, (ii, jj), d, ign=True)
                    g[ii][jj] = g[i][j]
                    g[i][j] = "."
                    return ii, jj
                return i, j
            if ign:
                if can_move(g, n, m, (ii, jj), d):
                    move(g, n, m, (ii, jj), d)
                    g[ii][jj] = g[i][j]
                    g[i][j] = "."
                    return ii, jj
                return i, j
            else:
                if can_move(g, n, m, (ii, jj), d) and can_move(g, n, m, (ii, jj-1), d):
                    move(g, n, m, (ii, jj), d)
                    move(g, n, m, (ii, jj-1), d)
                    g[ii][jj] = g[i][j]
                    g[ii][jj-1] = g[i][j-1]
                    g[i][j] = "."
                    g[i][j-1] = "."
                    return ii, jj
                return i, j
    return (i, j)

with PuzzleContext(year=2024, day=15) as ctx:
    ans1, ans2 = None, None

    a, b = ctx.groups
    b = b.replace("\n", "")
    
    g, n, m = to_grid(a)
    
    start = None
    for i in range(n):
        for j in range(m):
            if g[i][j] == "@":
                start = (i, j)
    assert start is not None

    curr = start
    for op in b:
        if op == "<":
            d = (0, -1)
        elif op == ">":
            d = (0, 1)
        elif op == "^":
            d = (-1, 0)
        else:
            d = (1, 0)
        curr = move(g, n, m, curr, d)

    ans1 = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] == "O":
                ans1 += 100*i + j

    ctx.submit(1, str(ans1) if ans1 else None)

    s = ""
    for c in a:
        if c == "\n":
            s += c
        elif c == "#":
            s += "##"
        elif c == "O":
            s += "[]"
        elif c == ".":
            s += ".."
        elif c == "@":
            s += "@."
        else:
            assert False
    g, n, m = to_grid(s)
    start = None
    for i in range(n):
        for j in range(m):
            if g[i][j] == "@":
                start = (i, j)
    assert start is not None

    curr = start
    for op in b:
        if op == "<":
            d = (0, -1)
        elif op == ">":
            d = (0, 1)
        elif op == "^":
            d = (-1, 0)
        else:
            d = (1, 0)
        curr = move(g, n, m, curr, d)

    ans2 = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] == "[":
                ans2 += 100*i + j

    ctx.submit(2, str(ans2) if ans2 else None)
