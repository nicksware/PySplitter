import sys

def parse_grid():
    """Parses the initial game grid state from stdin."""
    grid = []
    for _ in range(height):
        row = list(map(int, input().split()))
        grid.append(row)
    return grid

def find_empty_near_special(grid, num):
    """Finds an empty space near a special space (star or heart), prioritizing grouping with same numbers."""
    best_score = -1
    best_move = None
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1 or grid[y][x] > 1: # Check for empty or special space
                score = 0
                # Check nearby spaces for same numbers or special spaces to increase score
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if grid[ny][nx] == num:
                            score += 1
                        elif grid[ny][nx] > 1: # Star or heart space
                            score += 2
                if score > best_score:
                    best_score = score
                    best_move = (x, y)
    return best_move

def update_grid(grid, num, x, y):
    """Updates the grid state by placing the number and its mirror correctly."""
    # Place the number
    grid[y][x] = -1  # Mark this tile as filled
    # Calculate and place the mirrored number
    mirror_x = width - x - 1
    grid[y][mirror_x] = -1  # Mark the mirrored tile as filled

def is_valid_placement(grid, x, y):
    """Checks if the placement is valid (empty and not previously filled)."""
    if grid[y][x] > 0:  # 1 for empty, 2 for star, 3 for heart
        # Check mirrored position as well
        mirror_x = width - x - 1
        return grid[y][mirror_x] > 0
    return False

def find_valid_placement(grid, num):
    """Finds a valid placement for the number considering current grid state."""
    for y in range(height):
        for x in range(int(width / 2)):  # Only need to iterate over half due to mirroring
            if is_valid_placement(grid, x, y):
                return x, y
    return None  # No valid placement found

def main():
    global width, height, rounds
    width, height, rounds = map(int, input().split())
    grid = parse_grid()

    try:
        for _ in range(rounds):
            num1, num2 = map(int, input().split())

            move = find_valid_placement(grid, num1)
            if move:
                x, y = move
                print(f"{num1} {x} {y}")
                update_grid(grid, num1, x, y)
            else:
                print("# No valid move found, passing.")
    except EOFError:
        pass

if __name__ == "__main__":
    main()
