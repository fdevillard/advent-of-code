from typing import List, Dict, Tuple
from functools import partial
import sys

def is_possible_game(trials: List[Dict[str, int]], target_counts: Dict[str, int]) -> bool:
    for trial in trials:
        for color in target_counts:
            if trial.get(color, 0) > target_counts[color]:
                return False

    return True

def parse_trial(trial: str) -> Dict[str, int]:
    result = {}
    for component in trial.split(","):
        count, color = component.strip().split(" ")
        result[color.strip()] = int(count.strip())

    return result

def parse_game(game: str) -> Tuple[int, List[Dict[str, int]]]:
    game_id, game_data = game.split(":")
    game_id = int(game_id.split()[1].strip())

    trials = [
        parse_trial(trial.strip())
        for trial in game_data.strip().split(";")
    ]

    return game_id, trials

def possible_games_sum(line, target_counts: Dict[str, int]):
    game_id, trials = parse_game(line)
    if is_possible_game(trials, target_counts):
        return game_id

    return 0

if __name__ == "__main__":
    target_counts = {'red': 12, 'green': 13, 'blue': 14}


    result = sum(map(partial(possible_games_sum, target_counts=target_counts), sys.stdin))

    print(result)
