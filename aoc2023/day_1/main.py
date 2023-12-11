from core.input_reader import get_day_input

DIGITS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def digits(inp: str) -> str:
    """Converts a string to only its digit characters.

    >>> digits("test1four3e2test")
    >>> "132"
    """
    return "".join(d for d in inp if d.isdigit())


def first_last(inp: str) -> int:
    """Gets the first and last digit from a string as two-digit int.

    >>> first_last("test1four3e2test")
    >>> 12
    """
    dgs = digits(inp)
    return int(dgs[0] + dgs[-1])


def find_digit_str_pos(inp: str) -> tuple[int | None, int | None]:
    """Finds the first and last printed digit in a string that can be converted to a numerical digit.

    >>> find_digit_str_pos("4nineeightseven2")
    >>> (9, 7)
    """
    # Tracks the position of all digit string indices.
    firstpos = []
    lastpos = []

    # Fetches the index of the first occurrence of a digit string representation,
    # or -1 if that digit string is not present.
    for v in DIGITS:
        try:
            firstpos.append(inp.index(v))
        except ValueError:
            firstpos.append(-1)
        try:
            lastpos.append(inp.rindex(v))
        except ValueError:
            lastpos.append(-1)

    # Fetch the index of the minimum value from the list of positions, with each index
    # corresponding to its digit, excluding negatives.
    # E.G. [-1, -1, 1, 3, -1] -> 1, the index of the max value, which means that the string "two"
    # was the first detection.
    try:
        first = firstpos.index(min([p for p in firstpos if p >= 0]))
    except ValueError:
        first = None

    try:
        last = lastpos.index(max(p for p in lastpos if p >= 0))
    except ValueError:
        last = None

    return first, last


def convert_digit_strings(inp: str) -> str:
    """Converts the first and last printed digits in strings to numerical digits.

    >>> convert_digit_strings("4nineeightseven2")
    >>> "49eight72"
    """
    firstpos, lastpos = find_digit_str_pos(inp)
    if firstpos is not None:
        inp = inp.replace(DIGITS[firstpos], str(firstpos), 1)

    if lastpos is not None:
        inp = str(lastpos).join(inp.rsplit(DIGITS[lastpos], 1))

    return inp


def main():
    # Read Input
    day = 1
    lines = get_day_input(day).splitlines()

    # Part 1
    tot = 0
    for line in lines:
        tot += first_last(line)

    print(f"Part 1: {tot}")

    # Part 2
    tot = 0
    for line in lines:
        tot += first_last(convert_digit_strings(line))

    print(f"Part 2: {tot}")


if __name__ == "__main__":
    main()
