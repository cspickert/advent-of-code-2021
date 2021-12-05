import importlib
from argparse import ArgumentParser


def run(day_module):
    input_module = importlib.import_module("input")
    input_str = getattr(input_module, day_module)
    solution_module = importlib.import_module(day_module)
    solution_cls = getattr(solution_module, "Solution")
    solution = solution_cls()
    solution_input = solution.load_data(input_str)
    print(solution.part1(solution_input))
    solution_input = solution.load_data(input_str)
    print(solution.part2(solution_input))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("day_module", help="The day module to run, e.g. day01")
    args = parser.parse_args()
    run(args.day_module)
