import re

from core.input_reader import get_day_input


NUM_PATTERN = re.compile(r"\d+")
GEAR_PATTERN = re.compile(r"\*")


def is_symbol(ch: str) -> bool:
    """Returns whether a character is considered a "symbol" in the context of the problem.

    The logic used for this is that any character that is not a digit 0-9 and is not a "." is a symbol.

    >>> is_symbol("$")
    >>> True

    >>> is_symbol("1")
    >>> False
    """
    return not any([ch.isdigit(), ch == "."])


def parse_numbers(line: str) -> dict[tuple[int, int], int]:
    """Gets all numbers from a single string, keyed by the indices of that number.

    >>> parse_numbers("467..114..")
    >>> {(0, 2): 467, (5, 7): 114}
    """
    tokens = {}

    for match in re.finditer(NUM_PATTERN, line):
        tokens[(match.start(), match.end()-1)] = int(match.group())

    return tokens


def parse_gears(line: str) -> list[int]:
    """Finds the indices of all "gears" (asterisks) in a line.

    >>> parse_gears("123...*..$..34..*....12..")
    >>> [6, 16]
    """
    tokens = []

    for match in re.finditer(GEAR_PATTERN, line):
        tokens.append(match.start())

    return tokens


def has_adjacent_symbol(lines: list[str], line_index: int, number_indices: tuple[int, int]) -> bool:
    """Determines whether a symbol is adjacent to the indices of a specific number.

    In the context of the problem, this includes diagonals.
    """
    line_count = len(lines)

    # Iterate over the rows one before to one after the line that the number is on.
    for i in range(line_index - 1, line_index + 2):
        # Ensure that the row is within bounds.
        if 0 <= i < line_count:
            line_len = len(lines[i])
            # Iterate from the indices one before the number to one after to check for symbols.
            for x in range(number_indices[0]-1, number_indices[1] + 2):
                # Ensure the character index is in bounds.
                if 0 <= x < line_len:
                    # Check if the character is a symbol.
                    if is_symbol(lines[i][x]):
                        return True

    return False


def part_num_is_adjacent(gear_loc: tuple[int, int], number_loc: tuple[int, tuple[int, int]]) -> bool:
    """Determines whether a given gear index is within the range of what would be considered "adjacent"
    to a given part number index.

    >>> part_num_is_adjacent((1, 3), (0, (0, 2)))
    >>> True
    """
    # If the line number is not within one line different between the gear and number, they cannot be adjacent.
    # This performs the "vertical" verification of adjacency.
    if abs(gear_loc[0] - number_loc[0]) > 1:
        return False

    # Checks if the indices of any digits in the part number are within one index of the gear index.
    # This performs the "horizontal" verification of adjacency.
    return any([abs(gear_loc[1] - n) <= 1 for n in range(number_loc[1][0], number_loc[1][1] + 1)])


def check_gear_ratio(numbers: list[dict[tuple[int, int], int]], line_index: int, gear_i: int) -> int:
    """Checks if a given gear ("*") is considered a valid active gear, then returns the gear ratio
    of the gear if it is valid, or 0 if it is not."""

    line_count = len(numbers)
    adj_part_nums = []

    # Iterate from the line before to the line after the gear.
    for i in range(line_index - 1, line_index + 2):
        # Ensure line is within bounds
        if 0 <= i < line_count:
            # Iterate over all part numbers on the line.
            for indices, num in numbers[i].items():
                # Add the part number to the list of part numbers if it is adjacent.
                if part_num_is_adjacent((line_index, gear_i), (i, indices)):
                    adj_part_nums.append(num)

    # Valid gears will have exactly 2 adjacent part numbers.
    if len(adj_part_nums) == 2:
        # Multiply the part numbers and return the value.
        return adj_part_nums[0] * adj_part_nums[1]

    # Default return to 0 if there are not exactly 2 adjacent part numbers.
    return 0


def main():
    # Read Input
    day = 3
    lines = get_day_input(day).splitlines()

    # Part 1
    tot = 0
    tokens = [parse_numbers(l) for l in lines]
    for i, token in enumerate(tokens):
        for indices, num in token.items():
            if has_adjacent_symbol(lines, i, indices):
                tot += num

    print(f"Part 1: {tot}")

    # Part 2
    tot = 0
    numbers = [parse_numbers(l) for l in lines]
    tokens = [parse_gears(l) for l in lines]
    for i, token in enumerate(tokens):
        for gear_i in token:
            tot += check_gear_ratio(numbers, i, gear_i)

    print(f"Part 2: {tot}")


if __name__ == "__main__":
    main()
