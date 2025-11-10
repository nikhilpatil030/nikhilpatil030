import re


def decode_from_text(text_content):
    """Test function to decode from text content"""
    coordinates = []

    # Split by lines and parse each line
    lines = text_content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Try to match pattern: character x y
        parts = line.split()

        if len(parts) >= 3:
            # Last two parts should be numbers (x, y coordinates)
            try:
                y = int(parts[-1])
                x = int(parts[-2])
                # Everything before the last two parts is the character
                char = ' '.join(parts[:-2])
                coordinates.append((char, x, y))
            except ValueError:
                continue

    if not coordinates:
        print("Error: Could not parse any coordinates")
        return

    print(f"Parsed {len(coordinates)} coordinates")
    for char, x, y in coordinates[:5]:
        print(f"  '{char}' at ({x}, {y})")

    # Determine grid dimensions
    max_x = max(coord[1] for coord in coordinates)
    max_y = max(coord[2] for coord in coordinates)

    print(f"Grid dimensions: {max_x + 1} x {max_y + 1}")

    # Create grid filled with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Place characters at their specified positions
    for char, x, y in coordinates:
        grid[y][x] = char

    # Print the grid
    print("\nGrid output:")
    for row in grid:
        print(''.join(row))


# Test with the example data
with open('/home/user/nikhilpatil030/test_data.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    decode_from_text(text)
