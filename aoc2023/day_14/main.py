from core.input_reader import get_day_input


ROUND = "O"
SQUARE = "#"
SPACE = "."


# Processing
def load_eval(rocks: list[str]) -> int:
    """Evaluate the load for the rock column by subtracting each rounded rock index from the maximum load score
    and then summing the results.

    >>> load_eval([".O.". ".#.", "..#O", "..O."])
    >>> 7
    """
    max_load = len(rocks)
    return sum((max_load - i) * row.count(ROUND) for i, row in enumerate(rocks))


def transpose(pattern: list[str]) -> list[str]:
    """Flip the x and y axes of the input pattern.

    >>> transpose(["123", "456", "789"])
    >>> ["147", "258", "389"]
    """
    return ["".join(c) for c in zip(*pattern)]


def flip(pattern: list[str]) -> list[str]:
    """Flip the input on the x-axis.

    >>> flip(["123", "456", "789"])
    >>> ["321", "654", "987"]
    """
    return [row[::-1] for row in pattern]


def move(pattern: list[str]) -> list[str]:
    """Move all the ROUND characters as far as they can go to the start of their strings.

    >>> move([".#.O", ".O.O", "#.OO"])
    >>> [".#O.", "OO..", "#OO."]
    """
    rows = []
    for row in pattern:
        blocks = []
        # "#" characters are the immovable,
        # so split by those on each line and sort the contained "O" and "." characters.
        for block in row.split('#'):
            blocks.append(''.join(sorted(block, reverse=True)))
        rows.append('#'.join(blocks))

    return rows


def cycle(pattern: list[str], count: int) -> list[str]:
    """Cycle through a move to the North, West, South, and East for the board "count" number of times."""
    # Track a list of states that have been seen for when the states start to cycle.
    states = [pattern]

    for i in range(count):
        # The direction used in the movement requires the input to have rows and columns
        # switched before the first iteration, moving North. To then "rotate" the pattern so that we are going to move
        # West next with the same functions, we can flip the resulting sorted pattern instead of re-transposing
        # back to the original location. This effectively moves everything to the top edge of the current pattern,
        # then rotates the entire board 90 degrees clockwise, 4 times. This completes a cycle.
        for _ in range(4):
            pattern = transpose(pattern)
            pattern = move(pattern)
            pattern = flip(pattern)

        # If the state of the board after the cycle has been seen before, then we can find out at what point the
        # pattern started to loop around on itself, and calculate the index of the board state that would take place
        # at "count" cycles.
        if pattern in states:
            pattern_loop_start = states.index(pattern)
            return states[((count - pattern_loop_start) % (len(states) - pattern_loop_start)) + pattern_loop_start]

        # If the pattern has not been seen before, add it to the list of seen states.
        states.append(pattern)

    # If the loop completes without the pattern reaching a cycle, return the moved pattern.
    return pattern


def main() -> None:
    # Read Input
    day = 14
    lines = get_day_input(day).splitlines()

    # Part 1
    # Transpose the pattern, then perform the move,
    # then evaluate the load after transposing back.
    pattern = transpose(lines)
    pattern = move(pattern)
    load = load_eval(transpose(pattern))

    print(f"Part 1: {load}")

    # Part 2
    cycle_count = 1000000000
    pattern = cycle(lines, cycle_count)
    load = load_eval(pattern)

    print(f"Part 2: {load}")


if __name__ == "__main__":
    main()
