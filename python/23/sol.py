from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft
import networkx as nx


with PuzzleContext(year=2024, day=23) as ctx:
    g = nx.Graph()
    for l in ctx.nonempty_lines:
        parts = l.split("-")
        g.add_edge(parts[0], parts[1])

    ans1, ans2 = 0, ""
    for cl in nx.enumerate_all_cliques(g):
        if len(cl) == 3 and any(x[0] == "t" for x in cl):
            ans1 += 1
        pwd = ",".join(sorted(cl))
        if len(pwd) > len(ans2):
            ans2 = pwd

    ctx.submit(1, str(ans1) if ans1 else None)
    ctx.submit(2, str(ans2) if ans2 else None)
