import re
from math import lcm

from core.file_reader import read_file


INPUT_PATTERN = re.compile(r"(?P<loc>.{3}) = \((?P<left>.{3}), (?P<right>.{3})\)")
INST_MAP = ['L', 'R']


# Input Parsing
def parse_input(content: str) -> tuple[str, dict[str, tuple[str, str]]]:
    """Parses the raw problem input into a directions string and a dict containing the possible moves.

    >>> parse_input("...")
    >>> ('RRLLRLRLR', {"AAA": ("BBB", "ZZZ"), "BBB": ("ZZZ", "AAA")})
    """

    instructions, _, *maps = content.split("\n")

    maps = [INPUT_PATTERN.match(m) for m in maps]
    maps = {m.group('loc'): (m.group('left'), m.group('right')) for m in maps}

    return instructions, maps


# Processing
def count_steps_to_target(steps: str, maps: dict[str, tuple[str, str]]) -> int:
    loc = "AAA"
    target = "ZZZ"

    total_steps = len(steps)
    step_count = 0

    while loc != target:
        loc = maps[loc][0 if steps[step_count % total_steps] == "L" else 1]
        step_count += 1

    return step_count


def count_grouped_steps_to_target(steps: str, maps: dict[str, tuple[str, str]]) -> int:
    locs = [m for m in maps if m.endswith("A")]
    counts_to_hit_z = []

    total_steps = len(steps)

    for starting_loc in locs:
        step_count = 0

        loc = starting_loc
        while not loc.endswith("Z"):
            loc = maps[loc][0 if steps[step_count % total_steps] == "L" else 1]
            step_count += 1

        counts_to_hit_z.append(step_count)

    return lcm(*counts_to_hit_z)


def main(file_input: str) -> None:
    # Read Input
    content = read_file(file_input)
    instructions, maps = parse_input(content)

    # Part 1
    step_count = count_steps_to_target(instructions, maps)

    print(f"Part 1: {step_count}")

    # Part 2
    step_count = count_grouped_steps_to_target(instructions, maps)

    print(f"Part 2: {step_count}")


if __name__ == "__main__":
    main("./input.txt")
