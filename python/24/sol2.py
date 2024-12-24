from collections import defaultdict
from time import perf_counter_ns

MAX_SWAPS = 4

def key(a: str, b: str) -> tuple[str, str]:
    return min(a, b), max(a, b)

if __name__ == "__main__":
    wires: dict[tuple[str, str], dict[str, str]] = defaultdict(dict)
    with open("../../inputs/24.txt") as f:
        for l in f.read().split("\n\n")[1].split("\n"):
            if not l:
                continue
            x, target = l.split(" -> ")
            x, op, y = x.split()
            wires[key(x, y)][op] = target

    used = set()
    swaps = []

    def gen_ops(a: str, b: str, op_names: set[str], expected: dict[str, str]):
        k = key(a, b)
        ops = wires.get(k)
        if ops is None:
            return
        if set(ops.keys()) != op_names:
            return
        if any((k, op) in used for op in op_names):
            return
        
        values = {op: ops[op] for op in op_names}
        # if all expectation are met, return the value before trying any modifications
        if all(values[k] == v for k, v in expected.items()):
            for op in op_names:
                used.add((k, op))
            yield ops
            for op in op_names:
                used.remove((k, op))
        
        if len(swaps) >= 4:
            return
        
        for (x, y), other_ops in wires.items():
            for op2, t2 in other_ops.copy().items():
                if (key(x, y), op2) in used:
                    continue
                for op1 in op_names:
                    if key(x, y) == k and op2 == op1:
                        continue
                    t1 = ops[op1]
                    ops[op1] = t2
                    other_ops[op2] = t1
                    for op in op_names:
                        used.add((k, op))
                    swaps.append((t1, t2))
                    yield ops
                    swaps.pop()
                    for op in op_names:
                        used.remove((k, op))
                    ops[op1] = t1
                    other_ops[op2] = t2


    def half_adders(a: str, b: str, expected_s: str | None = None):
        exp = {}
        if expected_s is not None:
            exp["XOR"] = expected_s
        for s in gen_ops(a, b, {"XOR", "AND"}, exp):
            yield s["XOR"], s["AND"]

    def ors(a: str, b: str):
        for s in gen_ops(a, b, {"OR"}, {}):
            yield s["OR"]

    def full_adders(a: str, b: str, c: str, expected_s: str | None = None, expected_c: str | None = None):
        for s1, c1 in half_adders(a, b):
            for s2, c2 in half_adders(c, s1):
                if expected_s is None or s2 == expected_s:
                    for carry in ors(c1, c2):
                        if expected_c is None or carry == expected_c:
                            yield s2, carry

    def gen(c: str, start: int, end: int):
        def inner(i: int, c: str):
            if i == end:
                yield c
                return
            for _, c1 in full_adders(f"x{i:02}", f"y{i:02}", c, f"z{i:02}"):
                yield from inner(i+1, c1)

        return inner(start, c)
        

    t_start = perf_counter_ns()
    for _, c1 in half_adders("x00", "y00", "z00"):
        for cn in gen(c1, 1, 44):
            for s, c in full_adders("x44", "y44", cn, "z44", "z45"):
                ans2 = ",".join(sorted([
                    x
                    for pair in swaps
                    for x in pair
                ]))
                print("Swaps:", swaps)
                print("Part 2:", ans2)
                t_end = perf_counter_ns()
                dur_ns = t_end - t_start
                dur_ms = dur_ns / 10**6
                print(f"Duration: {dur_ms}ms")
                exit()



# with PuzzleContext(year=2024, day=24) as ctx:
#     ans1, ans2 = None, None

#     a, b = ctx.groups
#     d = {}
#     for l in a.split("\n"):
#         x, y = l.split(": ")
#         d[x] = y == "1"

#     def key(a: str, b: str) -> tuple[str, str]:
#         return min(a, b), max(a, b)

#     wires: dict[tuple[str, str], dict[str, str]] = defaultdict(dict)
#     for l in b.split("\n"):
#         x, target = l.split(" -> ")
#         x, op, y = x.split()
#         wires[key(x, y)][op] = target

    # used = set()
    # swaps = []

    # def half_adders(a: str, b: str, expected_s: str | None = None):
    #     k = key(a, b)
    #     ops = wires.get(k)
    #     if ops is None:
    #         return
    #     if {"XOR", "AND"} != set(ops.keys()):
    #         return
    #     if (k, "XOR") in used or (k, "AND") in used:
    #         return
    #     s = ops["XOR"]
    #     c = ops["AND"]
    #     s_is_as_expected = expected_s is None or s == expected_s
    #     if s_is_as_expected:
    #         # first, return the value that we already have and leave the generation for the future
    #         used.add((k, "XOR"))
    #         used.add((k, "AND"))
    #         yield s, c
    #         used.remove((k, "AND"))
    #         used.remove((k, "XOR"))
        
    #     if len(swaps) >= 4:
    #         return
        
    #     for (x, y), other_ops in wires.items():
    #         for op2, t2 in other_ops.copy().items():
    #             if (key(x, y), op2) in used:
    #                 continue
    #             for op1 in {"XOR", "AND"}:
    #                 if key(x, y) == k and op2 == op1:
    #                     continue
    #                 t1 = ops[op1]
    #                 ops[op1] = t2
    #                 other_ops[op2] = t1
    #                 used.add((k, "XOR"))
    #                 used.add((k, "AND"))
    #                 swaps.append((t1, t2))
    #                 yield ops["XOR"], ops["AND"]
    #                 swaps.pop()
    #                 used.remove((k, "AND"))
    #                 used.remove((k, "XOR"))
    #                 ops[op1] = t1
    #                 other_ops[op2] = t2

    # def ors(a: str, b: str):
    #     k = key(a, b)
    #     ops = wires.get(k)
    #     if ops is None:
    #         return
    #     if {"OR"} != set(ops.keys()):
    #         return
    #     if (k, "OR") in used:
    #         return
    #     yield ops["OR"]
        
    #     if len(swaps) >= 4:
    #         return
    #     for (x, y), other_ops in wires.items():
    #         if key(x, y) == k:
    #             continue
    #         for op2, t2 in other_ops.copy().items():
    #             if (key(x, y), op2) in used:
    #                 continue
    #             for op1 in {"OR"}:
    #                 t1 = ops[op1]
    #                 ops[op1] = t2
    #                 other_ops[op2] = t1
    #                 used.add((k, "OR"))
    #                 swaps.append((t1, t2))
    #                 yield ops["OR"]
    #                 swaps.pop()
    #                 used.remove((k, "OR"))
    #                 ops[op1] = t1
    #                 other_ops[op2] = t2

    # def full_adders(a: str, b: str, c: str, expected_s: str | None = None, expected_c: str | None = None):
    #     for s1, c1 in half_adders(a, b):
    #         for s2, c2 in half_adders(c, s1):
    #             if expected_s is None or s2 == expected_s:
    #                 for carry in ors(c1, c2):
    #                     if expected_c is None or carry == expected_c:
    #                         yield s2, carry

    # def gen(c: str, start: int, end: int):
    #     def inner(i: int, c: str):
    #         if i == end:
    #             yield c
    #             return
    #         for _, c1 in full_adders(f"x{i:02}", f"y{i:02}", c, f"z{i:02}"):
    #             yield from inner(i+1, c1)

    #     return inner(start, c)
        

    # for _, c1 in half_adders("x00", "y00", "z00"):
    #     for cn in gen(c1, 1, 44):
    #         for s, c in full_adders("x44", "y44", cn, "z44", "z45"):
    #             ans2 = ",".join(sorted([
    #                 x
    #                 for pair in swaps
    #                 for x in pair
    #             ]))
    #             print("Swaps:", swaps)
    #             print("Part 2:", ans2)
    #             exit()
