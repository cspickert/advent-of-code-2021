from base import BaseSolution

from collections import Counter


class Solution(BaseSolution):
    def load_data(self, input):
        return [list(line) for line in input.splitlines()]

    def part1(self, data):
        # Start with a matrix of strings
        # Transpose the matrix
        # Get the most and least frequent value in each row (gamma,
        # epsilon)
        # Transpose again
        # Convert rows to ints
        # Multiply

        transposed_data = [*zip(*data)]
        counted_rows = [
            [value for value, _ in Counter(row).most_common()]
            for row in transposed_data
        ]
        counted_rows_transposed = [*zip(*counted_rows)]
        gamma, epsilon = [int("".join(item), 2) for item in counted_rows_transposed]

        return gamma * epsilon

    def part2(self, data):
        pass
