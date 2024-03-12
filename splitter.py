import random

class Splitter:
    def __init__(self, width, height, rounds):
        self.width = width
        self.height = height
        self.rounds = rounds
        self.board = [[0] * width for _ in range(height)]
        self.score = 0

    def roll_dice(self):
        return random.randint(1, 6), random.randint(1, 6)

    def make_move(self, number, x, y):
        if self.board[y][x] != 0:
            return False
        self.board[y][x] = number
        return True

    def calculate_score(self):
        # Implement score calculation logic here
        pass

    def play_game(self):
        for _ in range(self.rounds):
            number1, number2 = self.roll_dice()
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            while not self.make_move(number1, x, y) or not self.make_move(number2, self.width - x - 1, y):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
        self.calculate_score()
        print("Game over! Final score:", self.score)

# Example usage:
if __name__ == "__main__":
    width = 8
    height = 7
    rounds = 22
    game = Splitter(width, height, rounds)
    game.play_game()
