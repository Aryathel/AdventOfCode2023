from core.input_reader import get_day_input


def transpose(pattern: list[str]) -> list[str]:
    return ["".join(row[i] for row in pattern) for i in range(len(pattern[0]))]


# Part 1
def find_symmetry_value(pattern: list[str]) -> int:
    """Evaluate an input pattern for its symmetry score.

    >>> find_symmetry_value(["..#.#", "##.#.", "##.#.", "..#.#"])
    >>> 200
    """
    # Evaluate vertical symmetry across all possible points of symmetry, returning 100 * the number of lines above
    # the point of symmetry if any are found.
    for r, row in enumerate(pattern[1:], 1):
        if has_symmetry(pattern, r):
            return 100 * r

    # Transpose the pattern so that the same symmetry check function can be used to evaluate horizontal symmetry.
    pattern = transpose(pattern)

    # Check for horizontal symmetry the same as vertical, but only returning the number of lines before the point of
    # symmetry if any are found rather than multiplying that value.
    for r, col in enumerate(pattern[1:], 1):
        if has_symmetry(pattern, r):
            return r

    # If no symmetry is found, return 0.
    return 0


def has_symmetry(pattern: list[str], index: int) -> bool:
    """Check if a pattern has symmetry around a given index.

    >>> has_symmetry(["..#.#", "##.#.", "##.#.", "..#.#"], 2)
    >>> True
    """
    # Use the entire pattern by default.
    row_start = 0
    row_end = None

    # Limit the indices to cut off lines that do not need to be checked for symmetry based off of whether
    # the index is in the first or second half of the pattern.
    if index < len(pattern) / 2:
        row_end = index * 2
    else:
        row_start = -(len(pattern) - index) * 2

    # Compare the first half of the pattern to the reversed second half to check for symmetry.
    return pattern[row_start:index] == list(reversed(pattern[index:row_end]))


# Part 2 - Very similar to part 1, but tweaked.
def find_near_symmetry_value(pattern: list[str]) -> int:
    """Evaluate an input pattern for its symmetry score.

    >>> find_near_symmetry_value(["..#.#", "##.#.", "##.#.", "#.#.#"])
    >>> 200
    """
    # Evaluate vertical symmetry across all possible points of symmetry. Check for places where there is only one
    # difference that would result in a true symmetry.
    for r, row in enumerate(pattern[1:], 1):
        if has_single_difference(pattern, r):
            return 100 * r

    # Transpose the pattern so that the same symmetry check function can be used to evaluate horizontal symmetry.
    pattern = transpose(pattern)

    # Check for horizontal symmetry the same as vertical, but only returning the number of lines before the point of
    # symmetry if any are found rather than multiplying that value.
    for r, col in enumerate(pattern[1:], 1):
        if has_single_difference(pattern, r):
            return r

    # If no symmetry is found, return 0.
    return 0


def has_single_difference(pattern: list[str], index: int) -> bool:
    """Check if a pattern has symmetry around a given index.

    >>> has_symmetry(["..#.#", "##.#.", "##.#.", "#.#.#"], 2)
    >>> True
    """
    # Use the entire pattern by default.
    row_start = 0
    row_end = None

    # Limit the indices to cut off lines that do not need to be checked for symmetry based off of whether
    # the index is in the first or second half of the pattern.
    if index < len(pattern) / 2:
        row_end = index * 2
    else:
        row_start = -(len(pattern) - index) * 2

    # Count the number of differences between the characters in the first and second half of the attempted symmetry.
    difference_count = 0
    # Iterate over each pair of rows
    for i, j in zip(pattern[row_start:index], list(reversed(pattern[index:row_end]))):
        # Iterate over each character pair in each row pair.
        for c1, c2 in zip(i, j):
            # If the characters do not match, it is a difference.
            if not c1 == c2:
                difference_count += 1
                # If there are more than 1 differences, return False.
                if difference_count > 1:
                    return False

    return difference_count == 1


def main() -> None:
    # Read Input
    day = 13
    lines = [l.splitlines() for l in get_day_input(day).split("\n\n")]

    # Part 1
    val = 0
    for pattern in lines:
        val += find_symmetry_value(pattern)

    print(f"Part 1: {val}")

    # Part 2
    val = 0
    for pattern in lines:
        val += find_near_symmetry_value(pattern)

    print(f"Part 2: {val}")


if __name__ == "__main__":
    main()
