import sys
from functools import partial, reduce
from typing import Dict, List, Tuple


def min_power_set(trials: List[Dict[str, int]]) -> int:
    min_values = {}
    for t in trials:
        for color, value in t.items():
            if value >= min_values.get(color, 0):
                min_values[color] = value

    return reduce(lambda a, b: a * b, min_values.values())


def parse_trial(trial: str) -> Dict[str, int]:
    result = {}
    for component in trial.split(","):
        count, color = component.strip().split(" ")
        result[color.strip()] = int(count.strip())

    return result


def parse_game(game: str) -> Tuple[int, List[Dict[str, int]]]:
    game_id, game_data = game.split(":")
    game_id = int(game_id.split()[1].strip())

    trials = [parse_trial(trial.strip()) for trial in game_data.strip().split(";")]

    return game_id, trials


def possible_games_sum(line):
    _, trials = parse_game(line)
    return min_power_set(trials)


if __name__ == "__main__":
    target_counts = {"red": 12, "green": 13, "blue": 14}

    result = sum(map(partial(possible_games_sum), sys.stdin))

    print(result)
