from core.file_reader import file_lines


# Input Parsing
def parse_line(line: str) -> list[int]:
    return list(map(int, line.split()))


# Processing
def reduce_pattern(pattern: list[int]) -> list[int]:
    """Reduces an input pattern into an output pattern by subtracting each pattern element from the previous
    value in the pattern.

    >>> reduce_pattern([10, 13, 16, 21, 30, 45, 68])
    >>> [3, 3, 5, 9, 15, 23]
    """
    return [val - pattern[i] for i, val in enumerate(pattern[1:])]


def find_next_value(pattern: list[int]) -> int:
    """Find the next value in a pattern by reducing the pattern repeatedly using the problem directions,
    then adding the last value in each reduced pattern to get the next value in the original pattern.

    >>> find_next_value([10, 13, 16, 21, 30, 45, 68])
    >>> 68
    """
    # Reduce the inpout pattern
    reduced = reduce_pattern(pattern)

    # Record the last value from the original pattern, and the last from the once reduced pattern.
    final_vals = [pattern[-1], reduced[-1]]

    # While any values in the reduced pattern are not 0
    while any(reduced):
        # Reduce the pattern again and add the last value in that pattern.
        reduced = reduce_pattern(reduced)
        final_vals.append(reduced[-1])

    # Sum the final value from each reduction of the pattern.
    return sum(final_vals)


def find_previous_value(pattern: list[int]) -> int:
    """Find the previous value in a pattern by reducing the pattern repeatedly,
    then subtracting/adding the first value in each reduced pattern to get the previous value.

    >>> find_previous_value([10, 13, 16, 21, 30, 45, 68])
    >>> 5
    """
    reduced = reduce_pattern(pattern)
    final_vals = [pattern[0], -reduced[0]]

    while any(reduced):
        reduced = reduce_pattern(reduced)

        # Looking at the pattern tree from the example, each value alternates between being added and subtracted for
        # each reduction. Therefore, we append either the positive or negative value depending on this.
        if len(final_vals) % 2 == 0:
            final_vals.append(reduced[0])
        else:
            final_vals.append(-reduced[0])

    # Sum all the positive and negative first values from each reduction.
    return sum(final_vals)


def main(file_input: str) -> None:
    # Read Input
    lines = file_lines(file_input)
    patterns = list(map(parse_line, lines))

    # Part 1
    val = 0
    for pattern in patterns:
        val += find_next_value(pattern)

    print(f"Part 1: {val}")

    # Part 2
    val = 0
    for pattern in patterns:
        val += find_previous_value(pattern)

    print(f"Part 2: {val}")


if __name__ == "__main__":
    main("./input.txt")
