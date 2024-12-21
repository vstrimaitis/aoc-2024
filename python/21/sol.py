from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

BUTTONS = [
    [
        list("789"),
        list("456"),
        list("123"),
        list(" 0A"),
    ],
    [
        list(" ^A"),
        list("<v>"),
    ]
]

@ft.cache
def bfs(start: tuple[int, int], goal: tuple[int, int], n_steps: int, mode: int) -> int:
    ans = 10**100
    buttons = BUTTONS[mode]
    gi, gj = goal
    q = deque()
    q.append((start, ""))
    while q:
        u, path = q.popleft()
        if u == goal:
            if mode == 0:
                ans = min(ans, solve(path + "A", n_steps, mode=1))
            else:
                ans = min(ans, solve(path + "A", n_steps-1, mode=1))
        elif buttons[u[0]][u[1]] == " ":
            continue
        else:
            i, j = u
            if i < gi:
                q.append(((i+1, j), path + "v"))
            elif i > gi:
                q.append(((i-1, j), path + "^"))
            if j < gj:
                q.append(((i, j+1), path + ">"))
            elif j > gj:
                q.append(((i, j-1), path + "<"))

    return ans

def solve(s: str, n_steps: int, mode: int = 0) -> int:
    assert 0 <= mode <= 1
    if mode == 1 and n_steps == 0:
        return len(s)

    btns = BUTTONS[mode]
    curr = grid_find(btns, "A")
    l = 0
    for c in s:
        target = grid_find(btns, c)
        l += bfs(curr, target, n_steps, mode)
        curr = target

    if mode == 0:
        return l * int(s[:-1])
    return l

with PuzzleContext(year=2024, day=21) as ctx:
    ans1, ans2 = 0, 0

    for l in ctx.nonempty_lines:
        ans1 += solve(l, 2)
        ans2 += solve(l, 25)

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
