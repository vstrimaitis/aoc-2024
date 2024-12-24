from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft

def solve(values: dict[str, bool], wires: list[tuple[str, str, str, str]]) -> int:
    rules = defaultdict(list)
    for x, op, y, target in wires:
        rules[(x, y)].append((op, target))
    values = values.copy()
    while rules:
        for (x, y), ls in rules.items():
            if x in values and y in values:
                for op, target in ls:
                    assert target not in values
                    a = values[x]
                    b = values[y]
                    if op == "AND":
                        values[target] = a and b
                    elif op == "OR":
                        values[target] = a or b
                    else:
                        values[target] = a ^ b
                rules.pop((x, y))
                break
    return int("".join([str(int(b)) for _, b in sorted([(a, b) for a, b in values.items() if a[0] == "z"], reverse=True)]), 2)

def flatten(d: dict[str, bool], wires: list[tuple[str, str, str, str]]) -> dict[str, str] | None:
    wires_by_target = {
        w[-1]: w for w in wires
    }
    deg = defaultdict(lambda: 0)
    adj = defaultdict(list)
    for x, _, y, z in wires:
        adj[x].append(z)
        adj[y].append(z)
        if x not in d:
            deg[z] += 1
        if y not in d:
            deg[z] += 1
    q = deque()
    for _, _, _, z in wires:
        if deg[z] == 0:
            q.append(z)
    
    values = {
        k: k
        for k in d.keys()
    }
    while q:
        z = q.popleft()
        x, op, y, z = wires_by_target[z]
        a = values[x]
        b = values[y]
        if op == "AND":
            res = f"({a}) & ({b})"
        elif op == "OR":
            res = f"({a}) | ({b})"
        else:
            res = f"({a}) ^ ({b})"
        values[z] = res
        for zz in adj[z]:
            deg[zz] -= 1
            if deg[zz] == 0:
                q.append(zz)
    if any(x > 0 for x in deg.values()):
        return None
    return values

        


    
    # while rules:
    #     psize = len(rules)
    #     for (x, y), ls in rules.items():
    #         if x in values and y in values:
    #             for op, target in ls:
    #                 assert target not in values
    #                 a = values[x]
    #                 b = values[y]
    #                 if op == "AND":
    #                     values[target] = f"({a}) & ({b})"
    #                 elif op == "OR":
    #                     values[target] = f"({a}) | ({b})"
    #                 else:
    #                     values[target] = f"({a}) ^ ({b})"
    #             rules.pop((x, y))
    #             break
    #     if len(rules) == psize:
    #         return None
    
    # return values

def to_bits(x: int,label: str, n: int) -> dict[str, bool]:
    b = {}
    for i in range(n):
        b[f"{label}{i:02}"] = bool(x % 2)
        x //= 2
    assert x == 0
    return b

with PuzzleContext(year=2024, day=24) as ctx:
    ans1, ans2 = None, None

    a, b = ctx.groups
    d = {}
    for l in a.split("\n"):
        x, y = l.split(": ")
        d[x] = y == "1"
    wires = []
    for l in b.split("\n"):
        x, target = l.split(" -> ")
        x, op, y = x.split()
        wires.append([x, op, y, target])
    
    ans1 = solve(d, wires)
    ctx.submit(1, str(ans1) if ans1 else None)


    from pprint import pprint
    import json
    from sympy.parsing import parse_expr
    def get_expected_expressions():
        def half_adder(a, b):
            return f"({a}) ^ ({b})", f"({a}) & ({b})"
        def full_adder(a, b, c):
            s1, cout1 = half_adder(a, b)
            s2, cout2 = half_adder(c, s1)
            return s2, f"({cout1}) | ({cout2})"

        s, carry = half_adder("x00", "y00")
        expected = [
            ("z00", s),
        ]
        for i in range(1, 45):
            # print("    ?", i)
            s, carry = full_adder(f"x{i:02}", f"y{i:02}", carry)
            expected.append((f"z{i:02}", s))
        expected.append(("z45", carry))
        return [(x, parse_expr(y)) for x, y in expected]
    EXPECTED = get_expected_expressions()
    def check():
        res = flatten(d, wires)
        if res is None:
            return "z00"
        
        for z, expr in EXPECTED:
            actual = parse_expr(res[z])
            if expr != actual:
                return z
        return None
    # print(check())

    offenders = []
    for i, (x, op, y, target) in enumerate(wires):
        if target[0] == "z" and op != "XOR" and target != "z45":
            offenders.append((target, i))
        
    offenders = sorted(offenders)

    def solve(idx: int, curr_swaps: list[tuple[str, str]], used: set[int]):
        print(idx, check(), curr_swaps)
        if idx >= len(offenders):
            for i in range(7,len(wires)):
                for j in range(len(wires)):
                    if i in used or j in used:
                        continue
                    curr_swaps.append((wires[i][-1], wires[j][-1]))
                    wires[i][-1], wires[j][-1] = wires[j][-1], wires[i][-1]
                    r = check()
                    print(i, j, r)
                    if r is None:
                        found = []
                        for a, b in curr_swaps:
                            found += [a, b]
                        print("!!!", ",".join(sorted(found)))
                        # print(curr_swaps)
                        # for w in wires:
                        #     x, op, y, z = w
                        #     print(f"{x} {op} {y} -> {z}")
                        exit()
                    wires[i][-1], wires[j][-1] = wires[j][-1], wires[i][-1]
                    curr_swaps.pop()
            return
        z, i = offenders[idx]
        assert i in used
        for j, (_, opp, _, zz) in enumerate(wires):
            if j in used:
                continue
            if opp != "XOR":
                continue
            wires[i][-1] = zz
            wires[j][-1] = z
            curr_swaps.append((z, zz))
            used.add(j)
            # print("  !", j)
            # r = check()
            # if r is None or r > z:
            r = check()
            if r is None or r > z:
                solve(idx+1, curr_swaps, used)
            used.remove(j)
            curr_swaps.pop()
            wires[i][-1] = z
            wires[j][-1] = zz
    solve(0, [], {i for _, i in offenders})

    ctx.submit(2, str(ans2) if ans2 else None)




