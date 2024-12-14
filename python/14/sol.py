from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

def sim(r, w, h, t):
    x, y, vx, vy = r
    for _ in range(t):
        x = (x + vx) % w
        y = (y + vy) % h
    return (x, y, vx, vy)

def sim_all(rs, w, h, t):
    return [sim(r, w, h, t) for r in rs]

def vis(r, w, h):
    brd = {(x, y) for x, y, *_ in r}
    for i in range(h):
        for j in range(w):
            if (j, i) in brd:
                print("#", end="")
            else:
                print(".", end="")
        print()
    
def to_s(r, w, h):
    brd = {(x, y) for x, y, *_ in r}
    lines = []
    for i in range(h):
        line = []
        for j in range(w):
            if (j, i) in brd:
                line.append("#")
            else:
                line.append(".")
        lines.append("".join(line))
    return "\n".join(lines)

with PuzzleContext(year=2024, day=14) as ctx:
    W = 101
    H = 103

    # input
    robots = []
    for l in ctx.nonempty_lines:
        robots.append(ints(l))
    
    # part1
    new_robots = sim_all(robots, W, H, t=100)
    cnt = [0, 0, 0, 0]
    for x, y, *_ in new_robots:
        if x == W//2 or y == H//2:
            continue
        is_left = x < W//2
        is_up = y < H//2
        q = int(is_left) + 2*int(is_up)
        cnt[q]+=1
    ans1 = 1
    for v in cnt:
        ans1 *= v

    ctx.submit(1, str(ans1) if ans1 else None)

    # part2
    # with open("dump.txt", "w") as f:
    #     for t in range(1, 10000):
    #         robots = sim_all(robots, W, H, t=1)
    #         f.write(f"After {t}:\n")
    #         f.write(to_s(robots, W, H))
    #         f.write("\n")

    t = 0
    while True:
        t += 1
        if t % 1000 == 0:
            print(f"{t}...")
        robots = sim_all(robots, W, H, t=1)
        pos = {(x, y) for x, y, *_ in robots}
        cnt_with_neighbours = 0
        for x, y, *_ in robots:
            ok = False
            for dx, dy in DIRS_4:
                xx = x+dx
                yy = y+dy
                if (xx, yy) in pos:
                    cnt_with_neighbours += 1
                    break
        
        # arbitrary guess
        if cnt_with_neighbours > len(robots)//2:
            # print(f"After {t}:")
            # vis(robots, W, H)
            # input("Continue?")
            ans2 = t
            break

    ctx.submit(2, str(ans2) if ans2 else None)
