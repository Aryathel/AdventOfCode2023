import re

from core.file_reader import read_file


MAP_KEY_PATTERN = re.compile(r"(?P<from>.+)-to-(?P<to>.+) map:")


# Classes
class MapRow:
    """Contains a single value range for a map.

    The logic can be treated as 'anything in the range "src_start" to "src_end" is shifted by "offset"
    to reach the output'.

    Anything not in the src range remains the same.
    """
    def __init__(
            self,
            src_start: int,
            dest_start: int = None,
            rng: int = None,

            src_end: int = None,
            offset: int = None,
    ):
        self.offset = offset
        self.src_start = src_start
        self.rng = rng
        self.src_end = src_end if src_end is not None else self.src_start + self.rng

        self.dest_start = dest_start if dest_start is not None else self.src_start + self.offset

        self.offset = self.dest_start - self.src_start
        self.dest_end = self.dest_start + self.offset

    def map_value(self, val: int) -> int | None:
        """Maps a single value range to its output value."""
        if self.src_start <= val < self.src_end:
            return val + self.offset

        return None

    def __repr__(self) -> str:
        return f"<MapRow src_start={self.src_start} src_end={self.src_end} offset={self.offset}>"


class AlmanacMap:
    """Contains a single mapping collection from one key to another."""
    from_key: str
    to_key: str
    maps: list[MapRow]

    def __init__(
            self,
            raw_map: str | None = None,
            from_key: str | None = None,
            to_key: str | None = None,
            maps: list[MapRow] | None = None
    ):
        self.maps = maps or []
        self.from_key = from_key
        self.to_key = to_key

        if raw_map:
            self.raw_map = raw_map

            self.read_keys()
            self.parse_map()

    @property
    def key_line(self):
        return self.raw_map.strip().split('\n')[0]

    @property
    def map_lines(self):
        return self.raw_map.strip().split('\n')[1:]

    def read_keys(self):
        """Reads the from key and to keys from the raw input."""
        match = MAP_KEY_PATTERN.match(self.key_line)
        self.from_key = match.group('from')
        self.to_key = match.group('to')

    def parse_map(self):
        """Reads the mapping ranges from the raw input."""
        for row in self.map_lines:
            dest_start, src_start, rng = (int(v.strip()) for v in row.split())
            self.maps.append(MapRow(src_start, dest_start, rng))

    def map_value(self, val: int) -> tuple[str, int | None]:
        """Get an output value from the map based on the input ID."""
        for m in self.maps:
            mapped_val = m.map_value(val)
            if mapped_val is not None:
                return self.to_key, mapped_val

        return self.to_key, val

    def __repr__(self) -> str:
        return f"<AlmanacMap from_key=\"{self.from_key}\" to_key=\"{self.to_key}\">"


class Almanac:
    """Contains a collection of mappings for finding secondary values for a certain seed."""
    almanac_maps: dict[str, AlmanacMap]
    master_map: AlmanacMap

    def __init__(self, raw_maps: list[str]):
        self.raw_maps = raw_maps

        self.parse_maps()

    @property
    def map_count(self) -> int:
        return len(self.almanac_maps)

    @property
    def map_keys(self) -> list[str]:
        return list(self.almanac_maps.keys())

    def parse_maps(self) -> None:
        """Reads the maps in from the raw text input."""
        almanac_maps = [AlmanacMap(m.strip()) for m in self.raw_maps]
        self.almanac_maps = {m.from_key: m for m in almanac_maps}

    def map_value(self, from_key: str, val: int) -> tuple[str | None, int | None]:
        """Determines the next value in the sequence of maps for a given starting key and ID."""
        if from_key in self.almanac_maps:
            return self.almanac_maps[from_key].map_value(val)
        return None, None

    def walk_value_map(self, key: str, val: int) -> tuple[str, int]:
        """Continues following IDs from a starting key and ID all the way to the last possible result."""
        while key is not None:
            mapped_key, mapped_val = self.map_value(key, val)

            if mapped_key is None:
                break

            key, val = mapped_key, mapped_val

        return key, val

    def __repr__(self) -> str:
        return f"<Almanac map_count={self.map_count} map_keys={self.map_keys}>"


# Input Parsing
def parse_input(content: str) -> tuple[list[int], Almanac]:
    """Read the complete input file into the starting seed IDs
    and the almanac used to map those seeds to their respective IDs.

    >>> parse_input(...)
    >>> [79, 14, 55, 13] <Almanac map_count=7 map_keys=['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity']>
    """
    segments = content.split('\n\n')

    seeds = [int(s.strip()) for s in segments[0].split(': ')[1].split(' ')]
    almanac = Almanac(segments[1:])
    return seeds, almanac

# Processing


def main():
    # Read Input
    content = read_file("input.txt")

    # Part 1
    seeds, almanac = parse_input(content)
    mapped_seed_values = [almanac.walk_value_map('seed', s) for s in seeds]
    val = min([v[1] for v in mapped_seed_values if v[0] == 'location'])

    print(f"Part 1: {val}")

    # Part 2
    val = None
    seeds, almanac = parse_input(content)

    # While this technically works, it is a very brute force method and takes *extremely* long to compute.
    for i in range(0, len(seeds), 2):
        st = seeds[i]
        cnt = seeds[i+1]
        end = st + cnt

        for s in range(st, end):
           cur = almanac.walk_value_map('seed', s)[1]
           val = cur if val is None or cur < val else val

    print(f"Part 2: {val}")


if __name__ == "__main__":
    main()
