from core.file_reader import read_file


# Parsing
def parse_input(content: str) -> tuple[list[int], list[list[tuple[int, int, int]]]]:
    """Reads input file content into a list of ints and a collection of mapping ranges."""

    seed_seg, *map_segs = content.strip().split('\n\n')

    seeds = list(map(int, seed_seg.split(': ')[-1].split()))

    maps = [list(map(lambda t: tuple(map(int, t.split())), m.splitlines()[1:])) for m in map_segs]

    return seeds, maps


# Processing
def map_seeds(seeds: list[int], maps: list[list[tuple[int, int, int]]]) -> list[int]:
    """Walk the list of seeds forward together as a group through each conversion step.

    >>> map_seeds([10, 5], [[(1, 5, 8)]])
    >>> [6, 1]
    """
    # Iterate over each conversion block in the input.
    for step in maps:
        stepped_seeds = []
        # Iterate over each seed to perform this tier of the conversion
        for s in seeds:
            # Read the destination, source value, and range length from each conversion range on the step.
            for dst, src, rng in step:
                # If the seed number is within the conversion range, perform the conversion.
                if s in range(src, src + rng):
                    stepped_seeds.append(dst + s - src)
                    break
            # If the loop was not broken, meaning the conversion was not completed,
            # do not modify the seed value.
            else:
                stepped_seeds.append(s)

            # For the next conversion block, update the seed list
            # to use the stepped seeds from the current block.
            seeds = stepped_seeds

    return seeds


def map_seed_ranges(seeds: list[int], maps: list[list[tuple[int, int, int]]]) -> list[tuple[int, int]]:
    """Walk the list of seed ranges forward together through each conversion step.

    Each seed range is split up and conversion is applied based on the conversion range it overlaps with:
    >>> map_seed_ranges([10, 5], [[(1, 5, 8)]])
    >>> [(6, 3), (13, 2)]
    """
    # Convert the list of ints into a list of tuples of seed start value and length of the seed range.
    seed_stack = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]

    # Iterate over conversion steps.
    for i, step in enumerate(maps):
        stepped_seed_ranges = []

        # Iterate using a stack in order to support splitting overlapping ranges.
        while seed_stack:
            s, srng = seed_stack.pop()
            # Iterate over conversion ranges.
            for dst, src, rng in step:
                # Find the potentially overlapping points
                intersect_start = max(s, src)
                intersect_end = min(s + srng, src + rng)

                # If there is an overlap, step the seed range using the conversion range.
                if intersect_start < intersect_end:
                    stepped_seed_ranges.append((dst + intersect_start - src, intersect_end - intersect_start))

                    # Add any excess seed range back to the stack to process.
                    if s < intersect_start:
                        seed_stack.append((s, intersect_start - s))
                    if s + srng > intersect_end:
                        seed_stack.append((intersect_end, s + srng - intersect_end))
                    break

            # If no overlapping ranges are mapped, append the unmodified range to the list.
            else:
                stepped_seed_ranges.append((s, srng))

        # Reset the seed stack with the updated ranges for the next conversion step.
        seed_stack = stepped_seed_ranges

    return seed_stack


def main():
    # Read Input
    content = read_file("input.txt")

    seeds, maps = parse_input(content)

    # Part 1
    mapped_seeds = map_seeds(seeds, maps)
    val = min(mapped_seeds)

    print(f"Part 1: {val}")

    # Part 2
    mapped_seed_ranges = map_seed_ranges(seeds, maps)
    val = min(sorted(mapped_seed_ranges))[0]

    print(f"Part 2: {val}")


if __name__ == "__main__":
    main()
