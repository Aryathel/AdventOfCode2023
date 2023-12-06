from core.file_reader import file_lines
from aoc2023.day_1.main import digits


CUBE_LIMITS = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


def parse_round(r: str) -> dict[str, int]:
    """Parses a single round text input into a dict of cube color and count.

    >>> parse_round("1 red, 2 green, 6 blue")
    >>> {"red": 1, "green": 2, "blue": 6}
    """
    rounds = [c.split(' ') for c in r.split(', ')]

    return {color.strip(): int(count) for count, color in rounds}


def merge_rounds(rounds: list[dict[str, int]]) -> dict[str, int]:
    """Gets the maximum number of cubes for each color from a list of rounds,
    to be used when confirming that a game is possible.

    >>> merge_rounds([{"red": 1, "green": 2, "blue": 6}, {"red": 3}, {"green": 4, "blue": 2}])
    >>> {"red": 3, "green": 4, "blue": 6}
    """
    totals = {}
    for r in rounds:
        for color, count in r.items():
            if color not in totals:
                totals[color] = count
            elif totals[color] < count:
                totals[color] = count
    return totals


def parse_line(line: str) -> tuple[int, dict[str, int]]:
    """Parses a complete game input line into its game number and the maximum number of cubes seen
    of each color.

    >>> parse_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    >>> 1, {"blue": 6, "red": 4, "green": 2}
    """
    game_seg, round_seg = line.split(': ')
    game = int(digits(game_seg))

    rounds_split = round_seg.split('; ')
    totals = merge_rounds([parse_round(r) for r in rounds_split])
    return game, totals


def is_game_possible(cube_totals: dict[str, int]) -> bool:
    """Determines if a given game is possible based on the number of cubes known to exist.

    >>> is_game_possible({"blue": 6, "red": 4, "green": 2})
    >>> True
    """
    for color, total in cube_totals.items():
        if CUBE_LIMITS[color] < total:
            return False

    return True


def multiply_list(vals: list[int]) -> int:
    """Get the product of all values in a list.

    >>> multiply_list([6, 4, 2])
    >>> 48
    """
    res = vals[0]
    for i in vals[1:]:
        res *= i
    return res


def main():
    # Read Input
    lines = file_lines("input.txt")

    # Part 1
    # Sum the game numbers of all possible games.
    tot = 0
    for line in lines:
        game, cube_totals = parse_line(line)
        # If the game is possible, add the game number to the running sum.
        if is_game_possible(cube_totals):
            tot += game

    print(f"Part 1: {tot}")

    # Part 2
    # Sum the products of the minimum number of cubes of each color for each game to be viable.
    tot = 0
    for line in lines:
        _, cube_totals = parse_line(line)
        tot += multiply_list(list(cube_totals.values()))

    print(f"Part 2: {tot}")


if __name__ == "__main__":
    main()
