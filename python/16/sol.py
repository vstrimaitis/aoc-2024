from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft
import networkx as nx

Dir = Literal["U", "D", "L", "R"]
Node = tuple[int, int, Dir]
Edge = tuple[Node, Node, int]

with PuzzleContext(year=2024, day=16) as ctx:
    ans1, ans2 = None, None

    g, n, m = to_grid(ctx.data)

    start = None
    goal = None
    dir_names = "URDL"
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    gr = nx.Graph()

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if g[i][j] == "S":
                start = (i, j, "R")
            elif g[i][j] == "E":
                goal = (i, j)
            if g[i][j] == "#":
                continue
            for k, d in enumerate(dir_names):
                node = (i, j, d)
                gr.add_node(node)
                
                d_cw = dir_names[(k + 1) % len(dir_names)]
                node_cw = (i, j, d_cw)

                d_ccw = dir_names[(k - 1) % len(dir_names)]
                node_ccw = (i, j, d_ccw)

                gr.add_edge(node, node_cw, weight=1000)
                gr.add_edge(node, node_ccw, weight=1000)

            for d, (di, dj) in zip(dir_names, dirs):
                if g[i+di][j+dj] != "#":
                    gr.add_edge((i, j, d), (i+di, j+dj, d), weight=1)
    assert start is not None
    assert goal is not None

    dists_from_start = nx.single_source_dijkstra_path_length(gr, start)
    dists_from_end = nx.multi_source_dijkstra_path_length(
        gr, [(*goal, d) for d in dir_names]
    )

    ans1 = dists_from_end[start]
    ctx.submit(1, str(ans1) if ans1 else None)

    ans2 = 0
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if g[i][j] == "#":
                continue
            found = False
            for d in dir_names:
                node = (i, j, d)
                l1 = dists_from_start.get(node, 10**100)
                l2 = dists_from_end.get(node, 10**100)
                if l1 + l2 == ans1:
                    found = True
            if found:
                ans2 += 1
    ctx.submit(2, str(ans2) if ans2 else None)
