from itertools import combinations
from typing import Iterator

from core.input_reader import get_day_input

GALAXY = "#"
SPACE = "."


# Processing
class Universe:
    """Tracks a "galaxy" reading and controls operations on it."""
    galaxies: list[str]

    # Tracks the expansion of the galaxy as a tuple of row & column indices, and a third value that indicates how
    # large each index should be treated as.
    expansion: tuple[list[int], list[int], int] | None= None

    def __init__(self, galaxies: list[str]):
        self.galaxies = galaxies

    def expand_coordinate(self, coordinate: tuple[int, int]) -> tuple[int, int]:
        """Applies the previous set universe expansion to a coordinate."""
        # If there is no meaningful expansion, do not modify the coordinate.
        if not self.expansion or self.expansion[2] <= 1:
            return coordinate

        # One row already exists from the expansion, so we need to remove that one.
        expansion_width = self.expansion[2] - 1

        # Find all expansion row indices less than the coordinate's row, then multiple that count by the width of
        # expansion and add it to the original coordinate.
        row = coordinate[0] + (sum(i < coordinate[0] for i in self.expansion[0]) * expansion_width)
        # Repeat the above process for the column.
        col = coordinate[1] + (sum(i < coordinate[1] for i in self.expansion[1]) * expansion_width)

        return row, col

    def galaxy_coordinates(self) -> list[tuple[int, int]]:
        """Get all coordinates for every galaxy in the current state of the universe, including expansion."""

        coords = []
        for coord, ch in self:
            if ch == GALAXY:
                coords.append(self.expand_coordinate(coord))
        return coords

    def raw_galaxy_rows_and_columns(self) -> tuple[list[int], list[int]]:
        """Gets the rows and columns from the original input universe that contain galaxies."""
        cols = []
        rows = []
        for coord, ch in self:
            if ch == GALAXY:
                if coord[0] not in rows:
                    rows.append(coord[0])
                if coord[1] not in cols:
                    cols.append(coord[1])

        return sorted(rows), sorted(cols)

    def rows_and_cols_to_expand(self) -> tuple[list[int], list[int]]:
        """Gets the row and column indices that only contain SPACE characters and not galaxies."""

        # Get all the rows and columns that contain a galaxy.
        galaxy_rows, galaxy_cols = self.raw_galaxy_rows_and_columns()

        rows_to_expand = [r for r in range(len(self.galaxies)) if r not in galaxy_rows]
        cols_to_expand = [c for c in range(len(self.galaxies[0])) if c not in galaxy_cols]

        return rows_to_expand, cols_to_expand

    def set_expansion_width(self, n: int) -> None:
        """Expands a galaxy based on the rule that and row or column in the galaxy map that does NOT include
        a GALAXY character should be size "n" instead.
        """

        rows, cols = self.rows_and_cols_to_expand()

        self.expansion = rows, cols, n

    @staticmethod
    def coordinate_distance(loc1: tuple[int, int], loc2: tuple[int, int]) -> int:
        """Gets the distance between two coordinates based on the minimum number of steps required to get from one
        to the other.

        >>> Universe.coordinate_distance((6, 1), (11, 5))
        >>> 9
        """
        return sum(map(lambda x1, x2: abs(x1 - x2), loc1, loc2))

    def __str__(self) -> str:
        """Used for displaying the galaxy in a command-line friendly(ish) way.

        >>> galaxy = Universe(["...", "#.#", "..#", "#.."])
        >>> print(galaxy)
        >>> ...
            #.#
            ..#
            #..
        """
        return '\n'.join(self.galaxies)

    def __iter__(self) -> Iterator[tuple[int, int, str]]:
        """Iterate over each coordinate in the input galaxy, returning its coordinate and the character that is there.

        >>> galaxy = Universe([".#."])
        >>> for coordinate, char in galaxy:
        >>>     print(coordinate, char)
        >>> (0, 0) .
        >>> (0, 1) #
        >>> (0, 2) .
        """
        for i, row in enumerate(self.galaxies):
            for j, ch in enumerate(row):
                yield (i, j), ch


def main() -> None:
    # Read Input
    day = 11
    universe = Universe(get_day_input(day).splitlines())

    # Part 1
    universe.set_expansion_width(2)
    coordinates = universe.galaxy_coordinates()
    # Use the itertools.combinations method to get all pairs of galaxy coordinates, sum the distance between each pair.
    total_min_dist = sum(Universe.coordinate_distance(*c) for c in combinations(coordinates, 2))

    print(f"Part 1: {total_min_dist}")

    # Part 2
    universe.set_expansion_width(1000000)
    coordinates = universe.galaxy_coordinates()
    total_min_dist = sum(Universe.coordinate_distance(*c) for c in combinations(coordinates, 2))

    print(f"Part 2: {total_min_dist}")


if __name__ == "__main__":
    main()
