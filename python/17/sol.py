from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft
from contextlib import contextmanager

# Part 1
def combo(a,b,c,op):
    if op <= 3:
        return op
    if op == 4:
        return a
    if op == 5:
        return b
    if op == 6:
        return c
    assert False

def run(a, b, c, prog):
    ip = 0
    while ip < len(prog):
        opcode = prog[ip]
        op = prog[ip+1]
        ip += 2
        match opcode:
            case 0:
                a = a // 2**combo(a,b,c,op)
            case 1:
                b ^= op
            case 2:
                b = combo(a, b, c, op) % 8
            case 3:
                if a == 0:
                    pass
                else:
                    ip = op
            case 4:
                b = b ^ c
            case 5:
                yield combo(a,b,c,op)%8
            case 6:
                b = a // 2**combo(a,b,c,op)
            case 7:
                c = a // 2**combo(a,b,c,op)
            case _:
                assert False

# Ints-to-code
def combo_str(op):
    if op <= 3:
        return str(op)
    if op == 4:
        return "a"
    if op == 5:
        return "b"
    if op == 6:
        return "c"
    assert False

def print_program(a, b, c, prog):
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"c = {c}")
    ip = 0
    while ip < len(prog):
        opcode = prog[ip]
        op = prog[ip+1]
        print(f"# {ip}: ")
        ip += 2
        match opcode:
            case 0:
                print(f"a //= 2**{combo_str(op)}")
            case 1:
                print(f"b ^= {op}")
            case 2:
                print(f"b = {combo_str(op)}%8")
            case 3:
                print(f"if a != 0:")
                print(f"    goto {op}")
            case 4:
                print(f"b = b ^ c")
            case 5:
                print(f"print({combo_str(op)} % 8)")
            case 6:
                print(f"b = a // 2 ** {combo_str(op)}")
            case 7:
                print(f"c = a // 2 ** {combo_str(op)}")
            case _:
                assert False

# Part 2
INF = 10**1000

@contextmanager
def filled_range(arr: list[str], l: int, val: list[str]):
    """
    Context manager that tries to write the value of val at the specified
    position, and recovers the previous value upon exit. Yielded value
    specifies whether the full replacement is valid (i.e. there are no
    conflicts with known bits).
    """
    prev = arr.copy()
    can_fill = True
    for i, x in enumerate(val, start=l):
        if 0 <= i < len(arr):
            if arr[i] != "?" and arr[i] != x:
                can_fill = False
            arr[i] = x
    yield can_fill
    for i, x in enumerate(val, start=l):
        if 0 <= i < len(arr):
            arr[i] = prev[i]

def gen_range(arr: list[str], l: int, r: int, filled_val: list[str] | None = None):
    """
    Generates all possible sequences that can be insterted at `arr[l:r]` by
    replacing `?` with either `0` or `1`. Modifies `arr` in place and returns
    it to the initial state after each iteration.
    """
    if filled_val is None:
        filled_val = []
    if l >= r:
        yield filled_val
        return
    possibilities = ["0", "1"] if arr[l] == "?" else [arr[l]]
    for p in possibilities:
        prev = arr[l]
        arr[l] = p
        filled_val.append(p)
        yield from gen_range(arr, l+1, r, filled_val)
        filled_val.pop()
        arr[l] = prev

def solve_part2(prog: list[int]) -> int:
    """
    a, b, c = ..., 0, 0
    # 00: 
    b = a%8
    # 02: 
    b ^= 1
    # 04: 
    c = a // 2 ** b
    # 06: 
    b ^= 4
    # 08: 
    a //= 2**3
    # 10: 
    b = b ^ c
    # 12: 
    print(b % 8)
    # 14: 
    if a != 0:
        goto 0
    """
    a_bits = list("000") + (["?"] * 3 * len(prog))
    def gen(prog_id: int) -> int:
        if prog_id >= len(prog):
            if "?" not in a_bits:
                # print("".join(a_bits), int("".join(a_bits), 2))
                return int("".join(a_bits), 2)
            return INF
        need = prog[prog_id]
        suffix_start = len(a_bits) - 3*(prog_id+1)
        suffix_end = suffix_start + 3
        ans = INF
        for suffix_bits in gen_range(a_bits, suffix_start, suffix_end):
            suffix = int("".join(suffix_bits), 2)  # a % 8
            b1 = suffix ^ 1  # b after step 02
            b2 = b1 ^ 4  # b after step 06

            # b2 ^ c = need (from step 04)
            # => c = need ^ b2
            c = need ^ b2
            c_bin = list(f"{c:03b}")
            c_start = suffix_start-b1
            with filled_range(a_bits, c_start, c_bin) as ok:
                if ok:
                    ans = min(ans, gen(prog_id+1))
        return ans

    return gen(0)

with PuzzleContext(year=2024, day=17) as ctx:

    a, b, c, *prog = ints(ctx.data)

    ans1 = ",".join(map(str, run(a,b,c,prog)))
    ctx.submit(1, str(ans1) if ans1 else None)
    
    ans2 = solve_part2(prog)
    ctx.submit(2, str(ans2) if ans2 else None)
