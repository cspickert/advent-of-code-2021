from base import BaseSolution


DIGITS_TO_PATTERNS = {
    0: frozenset({0, 1, 2, 4, 5, 6}),
    1: frozenset({2, 5}),
    2: frozenset({0, 2, 3, 4, 6}),
    3: frozenset({0, 2, 3, 5, 6}),
    4: frozenset({1, 2, 3, 5}),
    5: frozenset({0, 1, 3, 5, 6}),
    6: frozenset({0, 1, 3, 4, 5, 6}),
    7: frozenset({0, 2, 5}),
    8: frozenset({0, 1, 2, 3, 4, 5, 6}),
    9: frozenset({0, 1, 2, 3, 5, 6}),
}

PATTERNS_TO_DIGITS = {value: key for key, value in DIGITS_TO_PATTERNS.items()}


class Solution(BaseSolution):
    def load_data(self, input):
        return [
            [section.split(" ") for section in line.split(" | ")]
            for line in input.splitlines()
        ]

    def part1(self, data):
        return sum(
            len(output) in {2, 3, 4, 7} for _, outputs in data for output in outputs
        )

    def part2(self, data):
        return sum(self.solve(line) for line in data)

    def solve(self, line):
        inputs, outputs = line
        valid_mapping = self.find_valid_mapping(inputs)
        return sum(
            self.get_digit_for_signal(signal, valid_mapping) * (10 ** i)
            for i, signal in enumerate(reversed(outputs))
        )

    def find_valid_mapping(self, inputs):
        for possible_mapping in self.find_all_mappings(inputs):
            needed_digits = set(range(10))
            for signal in inputs:
                digit = self.get_digit_for_signal(signal, possible_mapping)
                if digit in needed_digits:
                    needed_digits.remove(digit)
            if not needed_digits:
                return possible_mapping
        raise Exception("No valid mapping")

    def find_all_mappings(self, inputs):
        return self.find_mappings_step_1(inputs)

    def find_mappings_step_1(self, inputs):
        # Step 1: try mapping 1 segments, plus the top of the 7 (there
        # are 2 configurations)
        seg_1 = self.get_signal_by_length(inputs, 2)
        seg_7 = self.get_signal_by_length(inputs, 3)

        top = next(iter(seg_7 - seg_1))
        top_right = next(iter(seg_1))
        bottom_right = next(iter(seg_1 - {top_right}))

        results = []
        results += self.find_mappings_step_2(inputs, top, top_right, bottom_right)
        results += self.find_mappings_step_2(inputs, top, bottom_right, top_right)
        return results

    def find_mappings_step_2(self, inputs, top, top_right, bottom_right):
        # Step 2: try mapping the other segments for the 4 (2 more
        # configurations)
        seg_4 = self.get_signal_by_length(inputs, 4)

        remaining = seg_4 - {top_right, bottom_right}
        top_left = next(iter(remaining))
        middle = next(iter(remaining - {top_left}))

        results = []
        results += self.find_mappings_step_3(
            inputs, top, top_right, bottom_right, top_left, middle
        )
        results += self.find_mappings_step_3(
            inputs, top, top_right, bottom_right, middle, top_left
        )
        return results

    def find_mappings_step_3(
        self, inputs, top, top_right, bottom_right, top_left, middle
    ):
        # Step 3: figure out the missing segments of the 8 (2 more
        # configurations)
        seg_8 = self.get_signal_by_length(inputs, 7)

        remaining = seg_8 - {top, top_right, bottom_right, top_left, middle}
        bottom_left = next(iter(remaining))
        bottom = next(iter(remaining - {bottom_left}))

        results = []
        results += [
            [top, top_left, top_right, middle, bottom_left, bottom_right, bottom]
        ]
        results += [
            [top, top_left, top_right, middle, bottom, bottom_right, bottom_left]
        ]
        return results

    def get_signal_by_length(self, inputs, length):
        return frozenset(next(signal for signal in inputs if len(signal) == length))

    def get_digit_for_signal(self, signal, mapping):
        pattern = frozenset({mapping.index(c) for c in signal})
        return PATTERNS_TO_DIGITS.get(pattern)
