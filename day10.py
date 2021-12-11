from base import BaseSolution


MAPPING = {"{": "}", "(": ")", "[": "]", "<": ">"}
PENALTY = {")": 3, "]": 57, "}": 1197, ">": 25137}
BONUS = {")": 1, "]": 2, "}": 3, ">": 4}


class IllegalCharError(Exception):
    def __init__(self, input_char):
        super().__init__(f"Illegal character")
        self.input_char = input_char


class IncompleteChunkError(Exception):
    def __init__(self, stack):
        super().__init__(f"Incomplete chunk")
        self.stack = stack


class Solution(BaseSolution):
    def load_data(self, input):
        return input.splitlines()

    def part1(self, data):
        illegal_score = 0
        for line in data:
            try:
                self.check_syntax(line)
            except IllegalCharError as exc:
                illegal_score += PENALTY[exc.input_char]
            except IncompleteChunkError:
                pass
        return illegal_score

    def part2(self, data):
        line_scores = []
        for line in data:
            try:
                self.check_syntax(line)
            except IllegalCharError:
                pass
            except IncompleteChunkError as exc:
                line_score = 0
                while exc.stack:
                    autocomplete_char = exc.stack.pop()
                    line_score *= 5
                    line_score += BONUS[autocomplete_char]
                line_scores.append(line_score)
        line_scores.sort()
        return line_scores[len(line_scores) // 2]

    def check_syntax(self, line):
        stack = []
        for input_char in line:
            if input_char in MAPPING:
                stack.append(MAPPING[input_char])
            elif stack and stack[-1] == input_char:
                stack.pop()
            else:
                raise IllegalCharError(input_char)
        if stack:
            raise IncompleteChunkError(stack)
