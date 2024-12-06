import csv
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import matplotlib.pyplot as plt

USERNAME = "vstrimaitis"
YEAR = 2024
PAST_YEARS = [2022, 2023]
PAST_KEYS = {
    year: f"__{USERNAME}__{year}__"
    for year in PAST_YEARS
}

@dataclass
class Highlight:
    text: str
    color: str

def last_not_none(arr: list[int | None]) -> int | None:
    for x in reversed(arr):
        if x is not None:
            return x
    return None

def read_past_results():
    results = dict()
    for year in PAST_YEARS:
        personal_year_results = dict()
        for day in range(1, 25+1):
            p = Path(f"./data/{year}/leaderboard/day_{day}.csv")
            if not p.exists():
                break
            pos = None
            with p.open("r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["user"] == USERNAME:
                        assert pos is None
                        pos = int(row["position"])
            personal_year_results[day] = pos
        results[PAST_KEYS[year]] = personal_year_results
    return results

def read_results():
    past_results = read_past_results()
    results = defaultdict(lambda: dict())
    for day in range(1, 25+1):
        results[day] = {}
        # attach previous year's result
        for k, res in past_results.items():
            if (r := res[day]) is not None:
                results[day][k] = r
        p = Path(f"./data/{YEAR}/leaderboard/day_{day}.csv")
        if not p.exists():
            continue
        with p.open("r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                results[day][row["user"]] = int(row["position"])

    return results

def plot(results, highlights: dict[str, Highlight], goal_position: int, cutoff_position: int = 100, output_file: Path | None = None, leaderboard_size: int = 200) -> None:
    all_users = set(
        user
        for r in results.values()
        for user in r.keys()
    )
    xs = sorted(results.keys())
    for user in all_users:
        ys = [results[x].get(user, None) for x in xs]
        alpha = 0.3
        linewidth = 1
        color = None
        if user in highlights:
            alpha = 1
            linewidth = 3
            color = highlights[user].color
            res = last_not_none(ys)
            plt.text(
                xs[-1]+0.5,
                res,
                highlights[user].text + f" ({res})",
                color=color,
                weight="bold"
            )
        plt.plot(xs, ys, alpha=alpha, linewidth=linewidth, color=color)
    plt.text(xs[-1]+0.5, goal_position, "goal", color="red", weight="bold")
    plt.axhline(y=goal_position, color="red", linestyle="dashed")

    plt.text(xs[-1]+0.5, cutoff_position, "cutoff", color="black", weight="bold")
    plt.axhline(y=cutoff_position, color="black", linestyle="dashed")

    plt.xlabel("Day")
    plt.ylabel("Position")
    plt.ylim(bottom=0, top=leaderboard_size)
    if leaderboard_size > 200:
        plt.yticks([1, *range(20, leaderboard_size+1, 20)])
    else:
        plt.yticks([1, *range(10, leaderboard_size+1, 10)])
    plt.gca().invert_yaxis()
    plt.margins(x=0)
    plt.tight_layout()
    if output_file:
        plt.savefig(output_file, dpi=200)
    else:
        plt.show()


if __name__ == "__main__":
    results = read_results()
    plot(
        results,
        highlights={
            "vstrimaitis": Highlight(
                text="2024 result",
                color="blue",
            ),
            PAST_KEYS[2023]: Highlight(
                text="2023 result",
                color="gray"
            ),
            PAST_KEYS[2022]: Highlight(
                text="2022 result",
                color="lightgray"
            ),
        },
        goal_position=50,
        output_file=Path("./leaderboard.png"),
        leaderboard_size=500,
    )
