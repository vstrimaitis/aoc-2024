from aocd.models import Puzzle

puzzle = Puzzle(year=${YEAR}, day=${DAY})

for i, e in enumerate(puzzle.examples):
    with open(f"s{i}.txt", "w") as f:
        f.write(e.input_data)
    if e.answer_a:
        with open(f"a{i}_a.txt", "w") as f:
            f.write(e.answer_a)
    if e.answer_b:
        with open(f"a{i}_b.txt", "w") as f:
            f.write(e.answer_b)
