import random

class Splitter:
    def __init__(self, width, height, rounds):
        self.width = width
        self.height = height
        self.rounds = rounds
        self.board = [[0] * width for _ in range(height)]
        self.score = 0
        self.changed_cells = set()

    def roll_dice(self):
        return random.randint(1, 6), random.randint(1, 6)

    def make_move(self, number, x, y):
        if self.board[y][x] != 0:
            return False
        self.board[y][x] = number
        self.changed_cells.add((x, y))
        return True

    def calculate_score(self, x, y, number):
        directions = [(1, 0), (0, 1)]
        score = 0
        for dx, dy in directions:
            count = 1
            nx, ny = x + dx, y + dy
            while 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx] == number:
                count += 1
                nx, ny = nx + dx, ny + dy
            if count >= number:
                score += number
        return score

    def play_game(self):
        for _ in range(self.rounds):
            number1, number2 = self.roll_dice()
            # Strategie: Kies een willekeurige locatie voor de hoogste waarde
            number = max(number1, number2)
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            while not self.make_move(number, x, y) or not self.make_move(number, self.width - x - 1, y):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
        for x, y in self.changed_cells:
            self.score += self.calculate_score(x, y, self.board[y][x])
        print("Game over! Final score:", self.score)

# Example usage:
if __name__ == "__main__":
    width = 8
    height = 7
    rounds = 22
    game = Splitter(width, height, rounds)
    game.play_game()
