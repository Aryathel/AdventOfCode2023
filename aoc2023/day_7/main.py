from enum import Enum

from core.file_reader import file_lines


# Define all possible cards, and can use the indices to order them for scoring.
CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
# Part 2 has a different card order.
PART_2_CARDS = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']


class HandType(Enum):
    """Enumerates all possible hand types and their scores to use for comparison."""
    high_card = 0
    one_pair = 1
    two_pair = 2
    three_of_a_kind = 3
    full_house = 4
    four_of_a_kind = 5
    five_of_a_kind = 6


# Input Parsing
def parse_line(line: str) -> tuple[str, int]:
    """Reads a single line into a card hand and the big on that hand.

    >>> parse_line("32T3K 765")
    >>> ("32T3K", 765)
    """
    hand, bid = line.split()
    return hand.upper(), int(bid)


# Processing
def character_counts(hand: str) -> dict[str, int]:
    """Gets the different characters and their occurrence counts for a given hand.

    >>> character_counts("32T3K")
    >>> {"3": 2, "2": 1, "T": 1, "K": 1}
    """
    counts = {}
    for ch in hand:
        if ch not in counts:
            counts[ch] = 0

        counts[ch] += 1

    return counts


def get_hand_type(hand: str, use_jokers: bool = False) -> HandType:
    """Gets the hand type for the given card hand.

    >>> get_hand_type("32T3K")
    >>> HandType.one_pair

    PART 2:
    If "use_jokers" is set to True, then add the number of Jokers to the highest card count before processing. In
    this example, "KTJJT" gets treated as "KTTTT".

    >>> get_hand_type("KTJJT")
    >>> HandType.four_of_a_kind
    """
    counts = character_counts(hand)

    # Joker handling
    # Since 3 and 4 of a kind hands are always worth more than one or two pair hands,
    # just add the number of jokers to the card count that is the largest and remove the Jokers from the counts.
    # Also, if all five cards are jokers, we will ignore handling those jokers and leave it as five of a kind.
    if use_jokers and "J" in counts and not counts["J"] == 5:
        j_count = counts.pop("J")
        highest_count = 0
        highest_char = None
        for ch, count in counts.items():
            if highest_char is None or count > highest_count:
                highest_char, highest_count = ch, count

        counts[highest_char] += j_count

    # '23456'
    if len(counts) == 5:
        return HandType.high_card
    # '22345'
    elif len(counts) == 4:
        return HandType.one_pair
    # '22234' OR '22334'
    elif len(counts) == 3:
        return HandType.three_of_a_kind if any(c > 2 for c in counts.values()) else HandType.two_pair
    # '22223' OR '22233'
    elif len(counts) == 2:
        return HandType.four_of_a_kind if any(c > 3 for c in counts.values()) else HandType.full_house
    # '22222'
    elif len(counts) == 1:
        return HandType.five_of_a_kind


def hand_to_int(hand: str, use_jokers: bool = False) -> int:
    """Converts a hand to an integer value by converting every character to a zero padded two digit string and
    joining them. These can then be used to compare hands with like types to determine a winner.

    # Internally calls 'int("0000000101")', because the 2 card has an index of 0 ("00") and 3 is index 1 ("01")
    >>> hand_to_int("22233")
    >>> 101

    >>> hand_to_int("AAAAA")
    >>> 1212121212
    """
    # In part 2, jokers are treated as the lowest scoring card.
    if use_jokers:
        return int(''.join(f"{PART_2_CARDS.index(c):-02}" for c in hand))
    else:
        return int(''.join(f"{CARDS.index(c):-02}" for c in hand))


def main():
    # Read Input
    lines = file_lines("./input.txt")
    hands = list(map(parse_line, lines))

    # Part 1
    # Sort the hands by a primary key of the value of the HandType and a secondary key of the hand value for like
    # hand types.
    sorted_hands = sorted(
        hands,
        key=lambda h: (get_hand_type(h[0]).value, hand_to_int(h[0])),
        reverse=False
    )
    # Multiply each bid in the sorted hands by its index + 1 and sum the results to get the winnings.
    winnings = sum((i + 1) * h[1] for i, h in enumerate(sorted_hands))

    print(f"Part 1: {winnings}")

    # Part 2
    # Perform the same sorting, with the added logic for Jokers.
    sorted_hands = sorted(
        hands,
        key=lambda h: (get_hand_type(h[0], use_jokers=True).value, hand_to_int(h[0], use_jokers=True)),
        reverse=False
    )
    # Multiply the winnings in the same way as part 1.
    winnings = sum((i + 1) * h[1] for i, h in enumerate(sorted_hands))

    print(f"Part 2: {winnings}")


if __name__ == "__main__":
    main()
