from time import time

from aoc2023 import *


def run_all_days():
    all_start = time()

    for i, method in enumerate(DAY_METHODS, 1):
        print(f"------ Day {i} ------")
        day_start = time()
        method(f"./aoc2023/day_{i}/input.txt")
        day_end = time()
        print(f"------ {day_end - day_start:.4} seconds ------", end="\n\n")

    all_end = time()
    print(f"Full Runtime: {all_end - all_start:.4} seconds")


if __name__ == "__main__":
    run_all_days()
