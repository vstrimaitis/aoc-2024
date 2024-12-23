from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft


with PuzzleContext(year=2024, day=23) as ctx:
    adj = defaultdict(lambda: set())
    for l in ctx.nonempty_lines:
        a, b = l.split("-")
        adj[a].add(b)
        adj[b].add(a)

    nodes = list(adj.keys())
    cliques = set()
    q = deque([(x,) for x in nodes])

    ans1, ans2 = 0, ""
    def on_clique(cl: tuple[str, ...]):
        global ans1, ans2
        if len(cl) == 3 and any(x[0] == "t" for x in cl):
            ans1 += 1
        pwd = ",".join(cl)
        if len(pwd) > len(ans2):
            ans2 = pwd

    while q:
        cl = q.popleft()
        on_clique(cl)
        for u in nodes:
            ok = True
            for v in cl:
                if v not in adj[u]:
                    ok = False
                    break
            if ok:
                if cl[-1] < u:
                    q.append(cl + (u,))

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
