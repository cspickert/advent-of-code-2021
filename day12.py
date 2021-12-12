from collections import Counter, defaultdict

from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        data = defaultdict(set)
        for line in input.splitlines():
            loc1, loc2 = line.split("-")
            data[loc1].add(loc2)
            data[loc2].add(loc1)
        return dict(data)

    def part1(self, data):
        self.revisit_small_node = False
        return len(self.find_paths(data))

    def part2(self, data):
        self.revisit_small_node = True
        return len(self.find_paths(data))

    def find_paths(self, data, node="start", path=None):
        path = [node] if path is None else (path + [node])
        if node == "end":
            return [path]
        all_paths = []
        for next_node in data[node]:
            if self.can_visit_node(next_node, path):
                all_paths += self.find_paths(data, next_node, path)
        return all_paths

    def can_visit_node(self, node, path):
        if node in path:
            if self.is_terminal_node(node):
                return False
            if node.isupper():
                return True
            if self.revisit_small_node:
                return not self.has_revisited_any_small_node(path)
            return False
        return True

    def is_terminal_node(self, node):
        return node == "start" or node == "end"

    def has_revisited_any_small_node(self, path):
        return any(
            count > 1
            for count in Counter(node for node in path if node.islower()).values()
        )
