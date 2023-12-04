from core.file_reader import file_lines
from day_1.main import digits


# Parsing
def parse_nums(inp: str) -> set[int]:
    """Convert a string input into a set of integers.

    >>> parse_nums(" 1 21 53 59 44")
    >>> {1, 21, 53, 59, 44}
    """
    return {int(i) for i in inp.strip().replace("  ", " ").split()}


def parse_line(line: str) -> tuple[int, set[int], set[int]]:
    """Reads the card number as well as the player draws and winning numbers from the input line.

    >>> parse_line("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1")
    >>> (3, {1, 21, 53, 59, 44}, {69, 82, 63, 72, 16, 21, 14, 1})
    """
    card_seg, num_seg = line.split(": ")
    card_num = int(digits(card_seg))

    draw_seg, win_seg = num_seg.split(" | ")

    draws = parse_nums(draw_seg)
    wins = parse_nums(win_seg)

    return card_num, draws, wins


# Processing
def determine_card_score(draws: set[int], wins: set[int]) -> int:
    """Determines the number of items from the player draws that are in the winning numbers.

    >>> determine_card_score({1, 21, 53, 59, 44}, {69, 82, 63, 72, 16, 21, 14, 1})
    >>> 2
    """
    # Gets the length of the intersections between the draws and the wins.
    win_count = len(draws & wins)
    # Returns the related score, starting at 1 and doubling in values for every winning number.
    return pow(2, win_count-1) if win_count else 0


def propagate_cards(cards: dict[int, dict[str, int]], card_num: int | None = None) -> dict[int, dict[str, int]]:
    """Add the card numbers down the chain according to the rule:
    Add the "copy" count of the card to the next n cards in the list,
    n being the count of winning numbers in the current card.

    >>> propagate_cards({1: {"win_count": 1, "copies": 1}, 2: {"win_count": 1, "copies": 1}})
    >>> {1: {"win_count": 1, "copies": 1}, 2: {"win_count": 1, "copies": 2}}
    """
    card_num = card_num or 1

    if cards[card_num]['win_count'] >= 0:
        for i in range(card_num+1, card_num+cards[card_num]['win_count']+1):
            cards[i]["copies"] += cards[card_num]["copies"]

    if card_num + 1 < len(cards):
        cards = propagate_cards(cards, card_num + 1)

    return cards


def total_card_count(cards: dict[int, dict[str, int]]) -> int:
    """Sums the total number of cards in a stack.

    >>> total_card_count({1: {"win_count": 1, "copies": 1}, 2: {"win_count": 1, "copies": 2}})
    >>> 3
    """
    tot = 0
    for card_data in cards.values():
        tot += card_data['copies']
    return tot


def main():
    # Read Input
    lines = file_lines("./input.txt")

    # Part 1
    tot = 0
    for line in lines:
        _, draws, wins = parse_line(line)
        tot += determine_card_score(draws, wins)

    print(f"Part 1: {tot}")

    # Part 2
    cards = {}
    for line in lines:
        card, draws, wins = parse_line(line)
        cards[card] = {
            "win_count": len(draws & wins),
            "copies": 1,
        }

    cards = propagate_cards(cards)
    count = total_card_count(cards)

    print(f"Part 2: {count}")


if __name__ == "__main__":
    main()
