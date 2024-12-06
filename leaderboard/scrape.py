from pathlib import Path
import requests
from dataclasses import dataclass
from datetime import timedelta
from collections import defaultdict

USER_AGENT = "@vstrimaitis"
CACHE_DIR = (Path("~") / ".cache" / "aoc_leaderboard").expanduser()
DATA_DIR = Path(__file__).parent / "data"

@dataclass
class LeaderboardEntry:
    part: int
    position: int
    solve_time: timedelta
    user: str

def get_url(year: int, day: int) -> str:
    return f"https://adventofcode.com/{year}/leaderboard/day/{day}"

def get_raw_leaderbaord(year: int, day: int) -> str | None:
    cache_path = CACHE_DIR / f"{year}_{day}.html"
    if cache_path.exists():
        print("Statement already downloaded - taking from cache")
        return cache_path.read_text()
    print("Downloading statement")

    r = requests.get(get_url(year, day), headers={"User-Agent": USER_AGENT})
    if r.status_code == 404:
        return None
    html = r.content.decode("utf-8")
    with open(cache_path, "w") as f:
        f.write(html)
    return html

def extract_leaderboard(year: int, day: int) -> list[LeaderboardEntry] | None:
    doc = get_raw_leaderbaord(year, day)
    if doc is None:
        return None
    import bs4
    bs = bs4.BeautifulSoup(doc, "html.parser")
    entries = bs.find_all("div", {"class": "leaderboard-entry"})
    if len(entries) != 200:
        raise ValueError(f"Expected to find 200 leaderboard entries, but found {len(entries)} - maybe the leaderboard isn't full yet?")
    res = []
    for part, part_entries in zip((1, 2), (entries[100:], entries[:100])):
        for entry in part_entries:
            username_el = entry.find("span", {"class": "leaderboard-userphoto"}).next_sibling
            is_anon = not isinstance(username_el, bs4.NavigableString) and "leaderboard-anon" in username_el.attrs.get("class", None)
            username = username_el.text
            if is_anon:
                username = username[1:-1]

            solve_time_str = entry.find("span", {"class": "leaderboard-time"}).text.split("  ")[1]
            h, m, s = [int(x) for x in solve_time_str.split(":")]

            leaderboard_pos = entry.find("span", {"class": "leaderboard-position"}).text.strip()[:-1]

            res.append(LeaderboardEntry(
                part=part,
                solve_time=timedelta(hours=h, minutes=m, seconds=s),
                user=username,
                position=int(leaderboard_pos),
            ))
    return res
    
    

if __name__ == "__main__":
    YEARS = [2022, 2023, 2024]
    DAYS = list(range(1, 25+1))
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    for year in YEARS:
        year_data_root = DATA_DIR / str(year)
        year_data_root.mkdir(exist_ok=True)
        for day in DAYS:
            print(f"Extracting year {year} day {day}")
            entries = extract_leaderboard(year, day)
            if entries is None:
                print("Leaderboard not found - exiting")
                break
            user_to_entries: dict[str, list[LeaderboardEntry]] = defaultdict(lambda: [])
            for e in entries:
                user_to_entries[e.user].append(e)
            
            data = []
            for username, user_entries in user_to_entries.items():
                row_data = {
                    "user": username,
                    "p1_position": None,
                    "p1_time": None,
                    "p2_position": None,
                    "p2_time": None,
                }
                for e in user_entries:
                    row_data[f"p{e.part}_position"] = e.position
                    row_data[f"p{e.part}_time"] = e.solve_time.seconds
                data.append(row_data)
            
            import csv
            with open(year_data_root / f"day_{day}.csv", "w") as f:
                writer = csv.writer(f)
                cols = ["user", "p1_position", "p1_time", "p2_position", "p2_time"]
                writer.writerow(cols)
                for row in data:
                    parts = [str(row[c] or "") for c in cols]
                    writer.writerow(parts)
            

