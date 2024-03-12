import sys

def parse_grid():
    """Parses the initial game grid state from stdin."""
    grid = []
    for _ in range(height):
        row = list(map(int, input().split()))
        grid.append(row)
    return grid

def update_grid(grid, num, x, y):
    """Updates the grid state by placing the number and its mirror correctly."""
    # Place the number
    grid[y][x] = -1  # Mark this tile as filled
    # Calculate and place the mirrored number
    mirror_x = width - x - 1
    grid[y][mirror_x] = -1  # Mark the mirrored tile as filled

def update_grid_for_evaluation(grid, num, x, y):
    """Updates the grid for evaluation purposes by placing the number and its mirror without permanently modifying the grid."""
    new_grid = [row[:] for row in grid]  # Make a deep copy of the grid
    mirror_x = width - x - 1
    # Mark the selected and mirrored positions as filled for this hypothetical move
    new_grid[y][x] = num
    new_grid[y][mirror_x] = num
    return new_grid

def score_move(grid, num, x, y):
    """Scores a move based on its strategic value."""
    score = 0
    # Apply the move hypothetically
    temp_grid = update_grid_for_evaluation(grid, num, x, y)

    # Scoring for group formation potential
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Check orthogonal directions
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            if temp_grid[ny][nx] == num:
                score += 10  # Increase score for each adjacent matching number
    
    # Special tile considerations
    if grid[y][x] == 2 or grid[y][width - x - 1] == 2:  # Star tile
        score += 20
    if grid[y][x] == 3 or grid[y][width - x - 1] == 3:  # Heart tile
        score += 15

    # Future flexibility could be evaluated here as well (more complex and left as an exercise)

    return score

def is_valid_placement(grid, x, y):
    """Checks if the placement is valid (empty and not previously filled)."""
    if grid[y][x] > 0:  # 1 for empty, 2 for star, 3 for heart
        # Check mirrored position as well
        mirror_x = width - x - 1
        return grid[y][mirror_x] > 0
    return False

def find_best_move(grid, num1, num2):
    """Finds the best move for the current dice roll by evaluating all valid placements."""
    best_score = -1
    best_move = None
    for y in range(height):
        for x in range(int(width / 2)):  # Consider half due to mirroring
            if is_valid_placement(grid, x, y):
                # Evaluate move for num1
                score1 = score_move(grid, num1, x, y)
                # Evaluate move for num2, as if num2 was placed at x, y and mirrored
                score2 = score_move(grid, num2, x, y)
                
                # Choose the move with the higher score
                if score1 > best_score:
                    best_score = score1
                    best_move = (num1, x, y)
                if score2 > best_score:
                    best_score = score2
                    best_move = (num2, x, y)
    return best_move

def main():
    global width, height, rounds
    width, height, rounds = map(int, input().split())
    grid = parse_grid()

    try:
        for _ in range(rounds):
            num1, num2 = map(int, input().split())
            move = find_best_move(grid, num1, num2)
            if move:
                num, x, y = move
                print(f"{num} {x} {y}")
                update_grid(grid, num, x, y)
            else:
                print("# No valid move found, passing.")
    except EOFError:
        pass

if __name__ == "__main__":
    main()
