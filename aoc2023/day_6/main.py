from math import ceil

from core.input_reader import get_day_input
from core.util_methods import product


# Input Parsing
def parse_line(line: str) -> list[int]:
    """Reads the numbers from a given line into a list.

    >>> parse_line("Time:      7  15   30")
    >>> [7, 15, 30]
    """
    num_seg = line.split(':')[1]
    return list(map(int, num_seg.split()))


# Processing
def calculate_distance(time_held: int, total_time: int) -> int:
    """Calculates the distance a boat will travel based on the time the button is held
    and the total time for the race.

    >>> calculate_distance(3, 7)
    >>> 12
    """
    # Time held also directly translates to speed,
    # so multiply that by the amount of time spent travelling.
    return time_held * (total_time - time_held)


def count_winning_times(time: int, record_distance: int) -> int:
    """Counts the number of record-beating times holding the button on the boat
    possible for a race of length time that travels farther than the record_distance.

    >>> count_winning_times(7, 9)
    >>> 2
    """
    min_time = None

    # By the symmetrical nature of the curve created by plotting out all possible times held,
    # it can be determined that we only need to look at half of the times held. This finds
    # the point at which we can stop iterating, the midpoint.
    mid_point = ceil((time + 1) / 2)

    for time_held in range(mid_point):
        # Find the distance travelled at the current amount of time held.
        if calculate_distance(time_held, time) > record_distance:
            # Update the minimum time held, then break iteration.
            min_time = time_held
            break

    # Determine the max time held that works by taking the symmetrical value of the current min time along the
    # total race time.
    max_time = time - min_time

    # Any values in between the two will travel greater distances, so this returns the number of numbers
    # that fall in the range min_time <= n <= max_time.
    return max_time - min_time + 1


def main():
    # Read Input
    day = 6
    time, distance = get_day_input(day).splitlines()
    time = parse_line(time)
    distance = parse_line(distance)

    # Part 1
    # Get all winning times.
    winning_time_counts = [count_winning_times(t, d) for t, d in zip(time, distance)]
    # Multiply the number of winning times for each race together.
    val = product(winning_time_counts)

    print(f"Part 1: {val}")

    # Part 2
    # Merge the parsed winning times and distances into one number.
    time = int(''.join(str(i) for i in time))
    distance = int(''.join(str(i) for i in distance))

    # Calculate number of winning times.
    winning_time_count = count_winning_times(time, distance)

    print(f"Part 2: {winning_time_count}")


if __name__ == "__main__":
    main()
