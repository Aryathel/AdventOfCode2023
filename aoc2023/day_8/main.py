import re
from math import lcm

from core.input_reader import get_day_input


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
    """Count the number of steps to reach a target "ZZZ" value from a "AAA" starting point using the
    steps provided and navigating through the maps provided.

    >>> count_steps_to_target("LR", {"AAA": ("AAA", "BBB"), "BBB": ("ZZZ", "AAA")})
    >>> 3
    """
    loc = "AAA"
    target = "ZZZ"

    total_steps = len(steps)
    step_count = 0

    while loc != target:
        loc = maps[loc][0 if steps[step_count % total_steps] == "L" else 1]
        step_count += 1

    return step_count


def count_grouped_steps_to_target(steps: str, maps: dict[str, tuple[str, str]]) -> int:
    """Check the number of steps to for all values in the map that end in "A" to all reach values in the map that
    end in "Z" at the same time.

    The observation that can be made here is that each starting value takes a certain number of steps to reach
    a value ending in Z, then cycles back to the start of its rotation. So by checking the number of steps
    to reach a value ending in Z for all values ending in A, then we can take the lowest common multiple
    of those step counts to get the total number of steps required.

    >>> # I don't feel like typing out a complete example for this one.
    """
    # Get all values ending with "A" to start from.
    locs = [m for m in maps if m.endswith("A")]
    counts_to_hit_z = []

    total_steps = len(steps)

    # Get the number of steps to hit a value ending in "Z" for all starting values.
    for starting_loc in locs:
        step_count = 0

        loc = starting_loc
        while not loc.endswith("Z"):
            loc = maps[loc][0 if steps[step_count % total_steps] == "L" else 1]
            step_count += 1

        counts_to_hit_z.append(step_count)

    # Return the lowest common multiple.
    return lcm(*counts_to_hit_z)


def main() -> None:
    # Read Input
    day = 8
    content = get_day_input(day)
    instructions, maps = parse_input(content)

    # Part 1
    step_count = count_steps_to_target(instructions, maps)

    print(f"Part 1: {step_count}")

    # Part 2
    step_count = count_grouped_steps_to_target(instructions, maps)

    print(f"Part 2: {step_count}")


if __name__ == "__main__":
    main()
