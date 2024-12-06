from pathlib import Path
import csv
from collections import defaultdict
import csv

DATA_DIR = Path(__file__).parent / "data"

def pos_to_score(pos: int) -> int:
    return 100-pos+1

def to_leaderboard(scores: dict[str, int]) -> list[tuple[int, int, str]]:
    assigned_pos = 1
    real_pos = 1
    prev_score = 10**100
    ans = []
    for user, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        if score != prev_score:
            assigned_pos = real_pos
        ans.append((assigned_pos, score, user))
        real_pos += 1
        prev_score = score
    return ans

if __name__ == "__main__":

    for year in [2022, 2023, 2024]:
        scores = defaultdict(lambda: 0)
        year_data_root = DATA_DIR / str(year)
        year_leaderboard_dir = year_data_root / "leaderboard"
        year_leaderboard_dir.mkdir(exist_ok=True)
        for day in range(1, 25+1):
            data_path = year_data_root / f"day_{day}.csv"
            if not data_path.exists():
                print("Finished")
                exit(0)
            with data_path.open() as f:
                reader = csv.DictReader(f)
                for row in reader:
                    p1_score = pos_to_score(int(row["p1_position"] or 101))
                    p2_score = pos_to_score(int(row["p2_position"] or 101))
                    scores[row["user"]] += p1_score + p2_score
            out_path = year_leaderboard_dir / f"day_{day}.csv"
            with out_path.open("w") as f:
                writer = csv.DictWriter(f, ["position", "user", "score"])
                writer.writeheader()
                for pos, score, user in to_leaderboard(scores):
                    writer.writerow({"position": pos, "score": score, "user": user})
