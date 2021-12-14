from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        coords_input, folds_input = input.split("\n\n")
        coords = [
            tuple(int(value) for value in line.split(","))
            for line in coords_input.splitlines()
        ]
        folds = [
            (axis, int(value))
            for axis, value in [
                line.split(" ")[-1].split("=") for line in folds_input.splitlines()
            ]
        ]
        return coords, folds

    def part1(self, data):
        coords, folds = data
        return len(set(self.fold(coords, folds[0])))

    def part2(self, data):
        coords, folds = data
        for fold in folds:
            coords = self.fold(coords, fold)
        return self.display(coords)

    def fold(self, coords, fold):
        axis, dist = fold
        translated_coords = [
            (x - dist if axis == "x" else x, y - dist if axis == "y" else y)
            for x, y in coords
        ]
        translated_folded_coords = [
            (-x if x > 0 and axis == "x" else x, -y if y > 0 and axis == "y" else y)
            for x, y in translated_coords
        ]
        folded_coords = [
            (x + dist if axis == "x" else x, y + dist if axis == "y" else y)
            for x, y in translated_folded_coords
        ]
        return folded_coords

    def display(self, coords):
        max_x = max(x for x, _ in coords)
        max_y = max(y for _, y in coords)
        grid = [[" "] * (max_x + 1) for y in range(0, max_y + 1)]
        for x, y in coords:
            grid[y][x] = "#"
        return "\n".join("".join(row) for row in grid)
