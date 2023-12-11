from time import time

from aoc2023 import *
from core.input_reader import save_day_inputs


def run_all_days():
    print(f"------ Getting Inputs for Days 1-{len(DAY_METHODS)} ------", end='\n\n')
    save_day_inputs(list(range(1, len(DAY_METHODS)+1, 1)))

    all_start = time()

    for i, method in enumerate(DAY_METHODS, 1):
        print(f"------ Day {i} ------")
        day_start = time()
        method()
        day_end = time()
        print(f"------ {day_end - day_start:.4} seconds ------", end="\n\n")

    all_end = time()
    print(f"Full Runtime: {all_end - all_start:.4} seconds")


if __name__ == "__main__":
    run_all_days()
