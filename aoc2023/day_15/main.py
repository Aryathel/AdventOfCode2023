from core.input_reader import get_day_input


# Processing
def hash_algorithm(code: str) -> int:
    """Apply the HASH algorithm as defined by the problem.

    Start the value at 0.
    Add the ASCII value of the character in the string to the value, multiply the value by 17, then find the remainder
    after dividing by 256. Repeat for all characters in the code.

    >>> hash_algorithm("rn=1")
    >>> 30
    """
    val = 0
    for ch in code:
        val = ((val + ord(ch)) * 17) % 256
    return val


def process_boxes(sequence: list[str]) -> dict[int, dict[str, int]]:
    """Process the boxes according to the algorithm."""
    boxes = {}
    for code in sequence:
        # Set a value based on the label, using that to find the box number and setting the labels value according
        # to the input.
        if '=' in code:
            label, val = code.split('=')
            box = hash_algorithm(label)
            if box not in boxes:
                boxes[box] = {}
            boxes[box][label] = int(val)
        # Remove the label from the box number found by hashing the label.
        elif '-' in code:
            label = code.rstrip('-')
            box = hash_algorithm(label)
            if box in boxes and label in boxes[box]:
                boxes[box].pop(label)

    return boxes


def eval_boxes(boxes: dict[int, dict[str, int]]) -> int:
    """Evaluate the score of the boxes based off of multiplying the box number, the position of the lens int the box,
    and the focal length of each lens and then summing the results.
    """
    score = 0
    for box_num, box in boxes.items():
        for i, focal_length in enumerate(box.values(), 1):
            score += (box_num + 1) * i * focal_length

    return score


def main() -> None:
    # Read Input
    day = 15
    sequence = get_day_input(day).split(',')

    # Part 1
    val = sum(map(hash_algorithm, sequence))

    print(f"Part 1: {val}")

    # Part 2
    boxes = process_boxes(sequence)
    val = eval_boxes(boxes)

    print(f"Part 2: {val}")


if __name__ == "__main__":
    main()
