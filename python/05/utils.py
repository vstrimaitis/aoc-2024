import math
import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Callable, Iterable, Any, List, TypeVar, Tuple, Dict, overload, cast, Union

sys.setrecursionlimit(100000)
T = TypeVar("T")
TA = TypeVar("TA")
TB = TypeVar("TB")

def sign(x: int) -> int:
    return 1 if x > 0 else -1 if x < 0 else 0

def lmap(func: Callable[[TA], TB], iterables: Iterable[TA]) -> List[TB]:
    return list(map(func, iterables))

def lfilter(func: Callable[[T], bool], iterables: Iterable[T]) -> List[T]:
    return list(filter(func, iterables))

def lreversed(iterables: List[T]) -> List[T]:
    return list(reversed(iterables))

@overload
def windows(it: str, size: int) -> Iterable[deque[str]]:
    ...

@overload
def windows(it: Iterable[T], size: int) -> Iterable[deque[T]]:
    ...

def windows(it: Union[str, Iterable[T]], size: int) -> Iterable[Union[deque[str], deque[T]]]:
    window = deque()
    for x in it:
        window.append(x)
        if len(window) > size:
            window.popleft()
        if len(window) == size:
            yield window

def min_max(l: Iterable[T]) -> Tuple[T, T]:
    return min(l), max(l)

def diff_list(x: List[T]) -> List[T]:
    return [b-a for a, b in zip(x, x[1:])]

def flatten(l: Iterable[Iterable[T]]) -> List[T]:
    return [i for x in l for i in x]

def ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"-?\d+", s))

def p_ints(s: str) -> List[int]:
    return lmap(int, re.findall(r"\d+", s))

def floats(s: str) -> List[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))

def p_floats(s: str) -> List[float]:
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))

def words(s: str) -> List[str]:
    return re.findall(r"[a-zA-Z]+", s)

def to_grid(s: str, cell_width: int = 1, h_spacing: int = 0) -> Tuple[List[List[str]], int, int]:
    ans = []
    lines = s.split("\n")
    m = None
    for line in lines:
        groups = [line[i:i+cell_width] for i in range(0, len(line), cell_width+h_spacing)]
        if m is None:
            m = len(groups)
        elif len(groups) != m:
            raise ValueError(f"Expected all rows to be of length {m}, but got {len(groups)}")
        ans.append(groups)
    return ans, len(ans), len(ans[0])

def print_grid(grid: List[List[str]], sep: str = "") -> None:
    for line in grid:
        print(*line, sep=sep)

DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS_8 = [(1, 1), (-1, -1), (1, -1), (-1, 1)] + DIRS_4
def get_neigh_coords(grid: List[List[Any]], i: int, j: int, dirs: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    n, m = len(grid), len(grid[0])
    ans = []
    for di, dj in dirs:
        ii = i + di
        jj = j + dj
        if 0 <= ii < n and 0 <= jj < m:
            ans.append((ii, jj))
    return ans

def get_neighs(grid: List[List[T]], i: int, j: int, dirs: List[Tuple[int, int]], fill=None) -> List[T]:
    n, m = len(grid), len(grid[0])
    ans = []
    for di, dj in dirs:
        ii = i + di
        jj = j + dj
        if 0 <= ii < n and 0 <= jj < m:
            ans.append(grid[ii][jj])
        else:
            ans.append(fill)
    return ans

# TODO: Linked List

class DSU:
    def __init__(self, n: int) -> None:
        self._n = n
        self._parents = [i for i in range(n)]
        self._sizes = [1]*n
        self._num_groups = n
    
    @property
    def num_groups(self) -> int:
        return self._num_groups

    @property
    def groups(self) -> List[List[int]]:
        grouped: Dict[int, List[int]] = defaultdict(lambda: [])
        for i in range(self._n):
            grouped[self.find(i)].append(i)
        return list(grouped.values())
    
    def group_of(self, x: int) -> List[int]:
        group = []
        for i in range(self._n):
            if self.find(i) == self.find(x):
                group.append(i)
        return group

    def find(self, a: int) -> int:
        if a == self._parents[a]:
            return a
        self._parents[a] = self.find(self._parents[a])
        return self._parents[a]

    def same(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)
    
    def unite(self, a: int, b: int) -> None:
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self._sizes[a] > self._sizes[b]:
            a, b = b, a
        self._sizes[b] += self._sizes[a]
        self._parents[a] = self._parents[b]
        self._num_groups -= 1

@overload
def lget(l: Iterable[T], i: int) -> T:
    ...

@overload
def lget(l: Iterable[Iterable[T]], i: Tuple[int, int]) -> T:
    ...

@overload
def lget(l: Iterable[Iterable[Iterable[T]]], i: Tuple[int, int, int]) -> T:
    ...

def lget(l, i):
    for index in i:
        l = l[index]
    return l

def lset(l, i, v):
    for index in i[:-1]:
        l = l[index]
    l[i[-1]] = v

@dataclass(init=True, repr=True, eq=True, order=True)
class Point2d:
    x: int
    y: int

    @property
    def negated(self) -> "Point2d":
        return Point2d(-self.x, -self.y)

    def __add__(self, other: "Point2d") -> "Point2d":
        return Point2d(self.x+other.x, self.y+other.y)

    def __sub__(self, other: "Point2d") -> "Point2d":
        return self + other.negated
    
    def dot(self, other: "Point2d") -> int:
        return self.x*other.x + self.y*other.y
    
    def dist(self, other: "Point2d") -> float:
        return math.sqrt(self.dist2(other))

    def man_dist(self, other: "Point2d") -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        return dx + dy

    def dist2(self, other: "Point2d") -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        return dx*dx + dy*dy


@dataclass
class Interval:
    l: int
    r: int

    @property
    def length(self) -> int:
        return max(0, self.r - self.l + 1)

    @property
    def is_empty(self) -> bool:
        return self.length == 0

    @classmethod
    def from_str(cls, s: str) -> "Interval":
        x, y = [int(x) for x in s.split("-")]
        return cls(x, y)
    
    def contains(self, other: "Interval") -> bool:
        return self.l <= other.l and other.r <= self.r
    
    def intersects(self, other: "Interval") -> bool:
        return not (self.r < other.l or self.l > other.r)

    def intersection(self, other: "Interval") -> "Interval":
        l = max(self.l, other.l)
        r = min(self.r, other.r)
        if r < l:
            l, r = 0, -1
        return Interval(l, r)
