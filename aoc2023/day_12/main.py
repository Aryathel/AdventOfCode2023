from core.input_reader import get_day_input

SAFE = "."
BROKEN = "#"
UNKNOWN = "?"


# Input Parsing
def parse_input(line: str) -> tuple[str, tuple[int, ...]]:
    springs, counts = line.split()
    return springs, tuple(map(int, counts.split(',')))


# Processing
cache = {}


def memoize(func):
    """A decorator for the combo count function to cache responses to optimize recursion."""
    def memo(hot_springs: str, blocks: tuple[int, ...]):
        """Take in the hot_springs map and the blocks of expected broken values, then returned the cached response
        if one exists for the input arguments, otherwise cache the calculated response and return the result."""
        # Return value in cache
        if (hot_springs, blocks) in cache:
            return cache[(hot_springs, blocks)]

        # Calculate the result
        result = func(hot_springs, blocks)
        # Cache the result
        cache[(hot_springs, blocks)] = result
        return result

    return memo


# Apply memoization
@memoize
def get_valid_combo_count(hot_springs: str, blocks: tuple[int, ...]) -> int:
    """Intended to be called recursively to check for valid blocks of hot springs that match the input.

    >>> get_valid_combo_count("???.###", (1,1,3))
    >>> 1
    """

    # If we have parsed through the entire hot springs map, but we still have expected blocks of broken springs
    # remaining, return 0, otherwise return 1 (indicating a valid combination).
    if hot_springs == "":
        return 1 if blocks == () else 0

    # If no more blocks of broken hot springs remain, but we have a broken hot spring left in the map,
    # return 0, otherwise return 1.
    if blocks == ():
        return 0 if BROKEN in hot_springs else 1

    count = 0

    # If the first character in the hot springs is part either SAFE or UNKNOWN, recurse the hot springs map
    # without the first character and the unmodified blocks.
    if hot_springs[0] in (SAFE, UNKNOWN):
        count += get_valid_combo_count(hot_springs[1:], blocks)

    # If the first character is either BROKEN or UNKNOWN
    if hot_springs[0] in (BROKEN, UNKNOWN):
        block = blocks[0]
        # If the block length is less than or equal to the length of the hot springs map (does not reach past the end)
        # And there is not a guaranteed SAFE character in the block we are looking at
        # And either the block length matches the length of the map, OR the value after the block we are looking at is
        # either safe or unknown, then add the recursion.
        if (block <= len(hot_springs)
                and SAFE not in hot_springs[:block]
                and (block == len(hot_springs)
                     or hot_springs[block] in (SAFE, UNKNOWN))):
            # Recurse the map after the completed block, also adding 1 to get rid of the character after the block that
            # we treat as safe, as well as the blocks without the first block we just mapped.
            count += get_valid_combo_count(hot_springs[block + 1:], blocks[1:])

    return count


def unfold(hot_spring: str, blocks: tuple[int]) -> tuple[str, tuple[int, ...]]:
    """Unfolds a row of input for part 2 of the problem. The map is multiplied by 5 and then joined with a "?", while,
    the blocks are simply multiplied by 5."""
    return UNKNOWN.join([hot_spring] * 5), blocks * 5


def main() -> None:
    # Read Input
    day = 12
    lines = get_day_input(day).splitlines()
    hot_springs = list(map(parse_input, lines))

    # Part 1
    val = 0
    for hot_spring in hot_springs:
        val += get_valid_combo_count(*hot_spring)

    print(f"Part 1: {val}")

    # Part 2
    val = 0
    for hot_spring in hot_springs:
        val += get_valid_combo_count(*unfold(*hot_spring))

    print(f"Part 2: {val}")


if __name__ == "__main__":
    main()
