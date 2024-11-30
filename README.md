# Advent of Code 2024 Solutions

Library used for data: <https://github.com/wimglenn/advent-of-code-data>.

Main things:

* Fetch your token ([help](https://github.com/wimglenn/advent-of-code-wim/issues/1))
* Save the value in `~/.config/aocd/token`

## Downloading inputs

```bash
# Today's data
aocd > in.txt

# Data of a specific puzzle
aocd 3 2024 > in.txt
```

## Starting a new day

There's a script to start a new day:

```bash
./new_day.sh $day_number
```

Running the script will create a new folder with the template files for a Python solution
under `python/<day_number>`.

## Running the solutions

* Go to the directory of the day you want to run (e.g. `cd python/04`)
* Run `python sol.py` to run the solution against your individual input
* ... or run `python sol.py X` to run the solution against the input stored in the file `sX.txt` in the same directory

Shortcut for starting a day:

```bash
./new_day.sh X && cd python/XX && code sol.py
```
