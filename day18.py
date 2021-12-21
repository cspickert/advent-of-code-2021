import functools
import json
import re

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return input.splitlines()

    def part1(self, data):
        expr = functools.reduce(self.add, data)
        return self.magnitude(expr)

    def part2(self, data):
        pass

    def add(self, value1, value2):
        return self.reduce(f"[{value1},{value2}]")

    def reduce(self, expr):
        while True:
            print(expr)
            result = self.explode(expr)
            if result != expr:
                expr = result
                continue
            result = self.split(expr)
            if result != expr:
                expr = result
                continue
            return result

    def explode(self, expr):
        depth = 0
        for i, c in enumerate(expr):
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
            if depth > 4:
                break

        if i == len(expr) - 1:
            return expr

        pair_start = i
        pair_end = i + expr[i:].index("]") + 1
        pair_left, pair_right = json.loads(expr[pair_start:pair_end])

        # Find value to the left.
        left_value = None
        left_value_end = pair_start
        while left_value_end >= 0 and not expr[left_value_end].isdigit():
            left_value_end -= 1
        if left_value_end >= 0:
            left_value_start = left_value_end
            left_value_end += 1
            while expr[left_value_start].isdigit():
                left_value_start -= 1
            left_value_start += 1
            left_value = int(expr[left_value_start:left_value_end])

        # Find value to the right.
        right_value = None
        right_value_start = pair_end
        while right_value_start < len(expr) and not expr[right_value_start].isdigit():
            right_value_start += 1
        if right_value_start < len(expr):
            right_value_end = right_value_start
            while expr[right_value_end].isdigit():
                right_value_end += 1
            right_value = int(expr[right_value_start:right_value_end])

        # Start with an empty result string.
        result = ""

        # Append the updated string to the left of the pair.
        if left_value is None:
            result += expr[:pair_start]
        else:
            result += (
                expr[:left_value_start]
                + str(left_value + pair_left)
                + expr[left_value_end:pair_start]
            )

        # Append 0.
        result += "0"

        # Append the updated string to the right of the pair.
        if right_value is None:
            result += expr[pair_end:]
        else:
            result += (
                expr[pair_end:right_value_start]
                + str(right_value + pair_right)
                + expr[right_value_end:]
            )

        # Return the result.
        return result

    def split(self, expr):
        for match in re.finditer(r"\d+", expr):
            value = int(match.group())
            if value >= 10:
                start, end = match.span()
                return (
                    expr[:start] + f"[{value // 2},{value - (value // 2)}]" + expr[end:]
                )
        return expr

    def magnitude(self, expr):
        if isinstance(expr, str):
            expr = json.loads(expr)
        left, right = expr
        return 3 * (left if isinstance(left, int) else self.magnitude(left)) + 2 * (
            right if isinstance(right, int) else self.magnitude(right)
        )
