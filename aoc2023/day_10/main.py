from core.input_reader import get_day_input


# Tracks the directions that a pipe segment connects to.
PIPES = {
    "|": ("N", "S"),
    "-": ("E", "W"),
    "L": ("N", "E"),
    "J": ("N", "W"),
    "7": ("S", "W"),
    "F": ("S", "E"),
}


class Field:
    """Tracks a field filled with pipes based on the input list of strings."""
    # Tracks the coordinate of the "S" character internally.
    _start: tuple[int, int] = None

    # Used for walking the pipe path.
    _next: tuple[int, int] | None = None
    _cur: tuple[int, int] = None
    _old: tuple[int, int] = None
    _first_step: tuple[int, int] = None

    def __init__(self, pipes: list[str]):
        self.pipes = pipes

    @property
    def start(self) -> tuple[int, int]:
        """Fetches the starting point ("S") from the field.

        >>> field = Field(["S-7", "|.|", "L-J"])
        >>> field.start
        >>> (0, 0)
        """
        if self._start is None:
            for i, r in enumerate(self.pipes):
                if 'S' in r:
                    self._start = i, r.index("S")

        return self._start

    def get_char(self, loc: tuple[int, int]) -> str | None:
        """Returns the character at a specified coordinate in the field, or None if an invalid coordinate is given.

        >>> field = Field(["F-7", "|.|", "L-J"])
        >>> field.get_char((1, 1))
        >>> "."
        """
        if loc and 0 <= loc[0] < len(self.pipes) and 0 <= loc[1] < len(self.pipes[loc[0]]):
            return self.pipes[loc[0]][loc[1]]
        return None

    def pipe_count(self) -> int:
        """Returns the length of the connected pipe loop that starts and ends at the start character.

        >>> field = Field(["S-7", "|.|", "L-J"])
        >>> field.pipe_count()
        >>> 8
        """
        # Try going in each of the cardinal directions from the starting point until one is successfully connected.
        cardinal_directions = [
            ("N", self.get_north(self.start)),
            ("W", self.get_west(self.start)),
            ("S", self.get_south(self.start)),
            ("E", self.get_east(self.start)),
        ]
        for d, loc in cardinal_directions:
            # Step through the pipe loop while recording the number of steps
            length = 1
            self._next = loc
            self._cur = self.start
            self._first_step = self._next

            while self._step():
                length += 1

            # If more than one step occurred, the pipe was successfully iterated, and the segment count can be returned.
            if length > 1:
                return length

    def pipe_area(self) -> float:
        """Find the area of the pipe using the Shoelace formula.

        >>> field = Field(["S-7", "|.|", "L-J"])
        >>> field.pipe_area()
        >>> 4.0
        """
        self._next = self._first_step
        self._cur = self.start

        # Get the two sums from the shoelace pattern for each corner of the pipe.
        sum1 = 0
        sum2 = 0

        old_vertex = self._cur

        while self._step():
            if self.get_char(self._cur) in "LJF7":
                sum1 += self._cur[1] * old_vertex[0]
                sum2 += self._cur[0] * old_vertex[1]
                old_vertex = self._cur

        sum1 += self.start[1] * old_vertex[0]
        sum2 += self.start[0] * old_vertex[1]

        # Return the result of the different between the two divided by 2 to complete the shoelace formula
        return abs(sum2 - sum1) / 2

    def internal_point_count(self) -> float:
        """Find the number of whole-number coordinates contained within the completed pipe loop ising Pick's theorem
        after calculating the area using the Shoelace formula.

        >>> field = Field(["S-7", "|.|", "L-J"])
        >>> field.internal_point_count()
        >>> 1.0
        """
        # Get the pip area.
        area = self.pipe_area()

        # Subtract half the pipe count and add one to the area to get the number of internal points within the pipes.
        return area - (self.pipe_count() / 2) + 1

    def _step(self) -> bool:
        """Used while walking the completed pipe. Finds the next pip location based on the self._cur coordinate
        and the self._old coordinate. Used for internal pipe iteration.
        """
        char = self.get_char(self._next)

        # Check if the character is within bounds and is a valid pipe character (exit on "." or "S").
        if not char or char not in PIPES:
            return False

        self._old = self._cur
        self._cur = self._next

        # Find the next connected pipe piece from this one.
        self._find_next()

        # If the next connected piece did not match, return False to stop stepping.
        if not self._next:
            return False

        # Pipe iteration was successful and can continue to be stepped.
        return True

    def _find_next(self) -> None:
        """Sets the self._next pipe location based off of the current pipe character and where the previous pipe segment
        is located in relation to the current one.

        Sets the self._next pipe value to None if the next piece is not a valid pipe piece or is the starting point.
        """
        # Get the current pipe character
        char = self.get_char(self._cur)

        # Get the directions that the current pipe piece connects to.
        dirs = PIPES.get(char)

        # If the pipe piece has no connections ("." or "S"), set the next coordinate to None and return.
        if not dirs:
            self._next = None
            return

        # Each pipe piece connects to two directions. here we identify which of those two directions is the one
        # that the previous coordinate was at, then navigate to the next one in the list.
        next_i = None
        for i, d in enumerate(dirs):
            if (d == "N" and self.is_north(self._old, self._cur))\
                    or (d == "S" and self.is_south(self._old, self._cur))\
                    or (d == "W" and self.is_west(self._old, self._cur))\
                    or (d == "E" and self.is_east(self._old, self._cur)):
                next_i = (i + 1) % 2
                break

        # If the pipe segment does not connect to the previous location, set the next coordinate to None and return.
        if next_i is None:
            self._next = None
            return

        # Set the next coordinate based on the current pipe piece and the direction we entered the pipe piece from.
        next_dir = dirs[next_i]
        if next_dir == "N":
            self._next = self.get_north(self._cur)
        elif next_dir == "S":
            self._next = self.get_south(self._cur)
        elif next_dir == "W":
            self._next = self.get_west(self._cur)
        elif next_dir == "E":
            self._next = self.get_east(self._cur)

    @staticmethod
    def get_south(loc: tuple[int, int]) -> tuple[int, int]:
        """Gets the next coordinate to the "south" of the input coordinate."""
        return loc[0] + 1, loc[1]

    @staticmethod
    def get_north(loc: tuple[int, int]) -> tuple[int, int]:
        """Gets the next coordinate to the "north" of the input coordinate."""
        return loc[0] - 1, loc[1]

    @staticmethod
    def get_west(loc: tuple[int, int]) -> tuple[int, int]:
        """Gets the next coordinate to the "west" of the input coordinate."""
        return loc[0], loc[1]-1

    @staticmethod
    def get_east(loc: tuple[int, int]) -> tuple[int, int]:
        """Gets the next coordinate to the "east" of the input coordinate."""
        return loc[0], loc[1] + 1

    @classmethod
    def is_south(cls, from_loc: tuple[int, int], to_loc: tuple[int, int]) -> bool:
        """Checks if the first coordinate is to the "south" of the second coordinate."""
        return from_loc == cls.get_south(to_loc)

    @classmethod
    def is_north(cls, from_loc: tuple[int, int], to_loc: tuple[int, int]) -> bool:
        """Checks if the first coordinate is to the "north" of the second coordinate."""
        return from_loc == cls.get_north(to_loc)

    @classmethod
    def is_west(cls, from_loc: tuple[int, int], to_loc: tuple[int, int]) -> bool:
        """Checks if the first coordinate is to the "west" of the second coordinate."""
        return from_loc == cls.get_west(to_loc)

    @classmethod
    def is_east(cls, from_loc: tuple[int, int], to_loc: tuple[int, int]) -> bool:
        """Checks if the first coordinate is to the "east" of the second coordinate."""
        return from_loc == cls.get_east(to_loc)


def main() -> None:
    # Read Input
    day = 10
    lines = get_day_input(day).splitlines()
    field = Field(pipes=lines)

    # Part 1
    furthest_distance = field.pipe_count() / 2

    print(f"Part 1: {furthest_distance:.0f}")

    # Part 2
    contained_pieces = field.internal_point_count()

    print(f"Part 2: {contained_pieces:.0f}")


if __name__ == "__main__":
    main()
