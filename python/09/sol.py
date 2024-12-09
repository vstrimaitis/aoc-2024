from collections import *
from typing import *
from heapq import *
from dataclasses import dataclass
from puzzle import PuzzleContext
from utils import *
import itertools as itt
import functools as ft


@dataclass
class File:
    id: int
    size: int
    position: int


Block = File | None


def from_map(disk_map: str) -> list[File]:
    files = []
    next_id = 0
    curr_pos = 0
    if len(disk_map) % 2 != 0:
        disk_map += "0"  # extra empty space at the end to ensure even length
    for i in range(0, len(disk_map), 2):
        file_size = int(disk_map[i])
        space_size = int(disk_map[i + 1])
        files.append(File(id=next_id, size=file_size, position=curr_pos))
        curr_pos += file_size + space_size
        next_id += 1
    return files


def to_blocks(files: list[File]) -> list[Block]:
    blocks = []
    for f in files:
        while len(blocks) < f.position:
            blocks.append(None)
        for _ in range(f.size):
            blocks.append(File(id=f.id, size=1, position=len(blocks)))
    return blocks


def to_str(blocks: list[Block]):
    parts = []
    for b in blocks:
        if b is None:
            s = "."
        else:
            s = str(b.id)
        parts.append(s)
    return "".join(parts)


def first_empty(blocks: list[Block], start_i: int | None = None) -> int:
    i = start_i or -1
    i += 1
    while blocks[i] is not None:
        i += 1
    return i


def last_nonempty(blocks: list[Block], start_i: int | None = None) -> int:
    i = start_i or len(blocks)
    i -= 1
    while blocks[i] is None:
        i -= 1
    return i


def calc_checksum(files: list[File]) -> int:
    curr_pos = 0
    files = sorted(files, key=lambda f: f.position)
    res = 0
    for f in files:
        while curr_pos < f.position:
            curr_pos += 1
        for _ in range(f.size):
            res += curr_pos * f.id
            curr_pos += 1
    return res


with PuzzleContext(year=2024, day=9) as ctx:
    ans1, ans2 = None, None

    files = from_map(ctx.data.strip())

    # part 1
    blocks = to_blocks(files)
    i = first_empty(blocks)
    j = last_nonempty(blocks)
    while i < j:
        assert blocks[i] is None
        assert blocks[j] is not None
        blocks[i], blocks[j] = blocks[j], blocks[i]
        blocks[i].position = i
        i = first_empty(blocks, i)
        j = last_nonempty(blocks, j)
    ans1 = calc_checksum([b for b in blocks if b is not None])
    ctx.submit(1, str(ans1))

    # part 2
    for i, f in enumerate(reversed(files.copy())):
        if (i+1) % 100 == 0:
            print(f"{i+1}/{len(files)}")
        found_pos = None
        for f1, f2 in zip(files, files[1:]):
            space_start = f1.position + f1.size
            space_end = f2.position - 1
            space_size = space_end - space_start + 1
            if space_start > f.position:
                break
            if space_size >= f.size:
                found_pos = space_start
                break
        if found_pos is not None:
            files.remove(f)
            files.append(File(id=f.id, size=f.size, position=found_pos))
            files = sorted(files, key=lambda f: f.position)
    ans2 = calc_checksum(files)
    ctx.submit(2, str(ans2))
