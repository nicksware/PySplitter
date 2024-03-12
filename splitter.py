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

def game_progress(round):
    """Returns the game progress as a fraction."""
    return round / rounds

def adjust_score_for_progress(score, round, is_special):
    """Adjusts score based on game progression and whether the move uses a special tile."""
    progress = game_progress(round)
    if is_special:
        return score * (1 + progress)  # Increase the importance of special tiles as the game progresses
    else:
        return score

def dfs_count(grid, x, y, num, visited):
    """Depth-first search to count the number of adjacent tiles with the same value."""
    if x < 0 or x >= width or y < 0 or y >= height:
        return 0  # Out of bounds
    if visited[y][x] or grid[y][x] != num:
        return 0  # Already visited or not matching number
    visited[y][x] = True  # Mark as visited
    count = 1  # Count this tile
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Check all four directions
        count += dfs_count(grid, x + dx, y + dy, num, visited)
    return count

def completes_group(grid, num, x, y):
    """Checks if placing a number completes a group exactly."""
    visited = [[False for _ in range(width)] for _ in range(height)]
    count = dfs_count(grid, x, y, num, visited)
    return count == num

def board_state_analysis(grid):
    total_tiles = width * height
    filled_tiles = sum(row.count(-1) for row in grid)
    board_fullness = filled_tiles / total_tiles

    # Check for unused special tiles
    special_tiles_unused = sum(row.count(2) + row.count(3) for row in grid)

    return board_fullness, special_tiles_unused

def dynamic_special_tile_score(grid, x, y, round, num):
    progress = game_progress(round)
    board_fullness, special_tiles_unused = board_state_analysis(grid)
    is_special = grid[y][x] in [2, 3] or grid[y][width - x - 1] in [2, 3]
    base_score = 20 if is_special else 0

    if completes_group(grid, num, x, y):
        base_score *= 2  # Increase score for completing a group

    # Increase priority of special tiles as the board gets fuller
    if board_fullness > 0.75 and special_tiles_unused > 0:
        base_score *= 2  # Double the score if the board is getting full and special tiles are unused

    # Adjustments based on game progress
    elif progress > 0.5:
        base_score *= 1.5  # Increase score in the later half of the game

    return base_score

def empty_neighbors(grid, x, y):
    """Counts the empty neighbors around a given position."""
    count = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 1:
            count += 1
    return count

def score_move(grid, num, x, y, round):
    score = 0
    temp_grid = update_grid_for_evaluation(grid, num, x, y)

    # Basic scoring based on adjacency and group formation
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and temp_grid[ny][nx] == num:
            score += 5  # Score for adjacency

    # Enhanced dynamic scoring considering board state
    score += dynamic_special_tile_score(grid, x, y, round, num)

    # Reward moves that leave options open
    score += empty_neighbors(temp_grid, x, y) * (1 if round < rounds / 2 else 1.5)

    return score

def is_valid_placement(grid, x, y):
    """Checks if the placement is valid (empty and not previously filled)."""
    if grid[y][x] > 0:  # 1 for empty, 2 for star, 3 for heart
        # Check mirrored position as well
        mirror_x = width - x - 1
        return grid[y][mirror_x] > 0
    return False

def find_best_move(grid, num1, num2, current_round):
    """Finds the best move for the current dice roll by evaluating all valid placements."""
    best_score = -1
    best_move = None
    for y in range(height):
        for x in range(int(width / 2)):  # Consider half due to mirroring
            if is_valid_placement(grid, x, y):
                # Evaluate moves for num1 and num2, considering the round for dynamic adjustments
                score1 = score_move(grid, num1, x, y, current_round)
                score2 = score_move(grid, num2, x, y, current_round)
                
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
    current_round = 0

    try:
        for _ in range(rounds):
            num1, num2 = map(int, input().split())
            current_round += 1
            move = find_best_move(grid, num1, num2, current_round)
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
