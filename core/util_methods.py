from functools import reduce


def product(vals: list[int | float]) -> int | float:
    """Get the product of all values in a list.

    >>> product([1, 2, 3, 4])
    >>> 24
    """
    return reduce(lambda x, y: x * y, vals)
