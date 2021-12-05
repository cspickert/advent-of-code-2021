from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        all_inputs = input.split("\n\n")
        numbers_input, *board_inputs = all_inputs
        numbers = [int(value) for value in numbers_input.split(",")]
        boards = [self.parse_board(board_input) for board_input in board_inputs]
        return numbers, boards

    def part1(self, data):
        numbers, boards = data
        fastest_board, _, last_number = min(
            (self.play_bingo(numbers, board) for board in boards),
            key=lambda result: result[1],
        )
        return self.sum_unmarked_numbers(fastest_board) * last_number

    def part2(self, data):
        numbers, boards = data
        slowest_board, _, last_number = max(
            (self.play_bingo(numbers, board) for board in boards),
            key=lambda result: result[1],
        )
        return self.sum_unmarked_numbers(slowest_board) * last_number

    def parse_board(self, board_input):
        return [
            [int(value) for value in line.split(" ") if value]
            for line in board_input.splitlines()
        ]

    def play_bingo(self, numbers, board):
        for step, number in enumerate(numbers, start=1):
            for row in range(len(board)):
                for col in range(len(board[row])):
                    if board[row][col] == number:
                        # Mark called numbers by destructively setting
                        # `board[row][col]` to `None`.
                        board[row][col] = None
                        if step >= 5 and self.check_board(board):
                            return board, step, number

    def check_board(self, board):
        return any(self.check_row(row) for row in board) or any(
            self.check_row(row) for row in zip(*board)
        )

    def check_row(self, row):
        return all(value is None for value in row)

    def sum_unmarked_numbers(self, board):
        return sum(number for row in board for number in row if number is not None)
