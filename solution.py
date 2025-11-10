"""
Solution for Decoding a Secret Message

This script takes a Google Doc URL containing Unicode characters and their 2D coordinates,
retrieves the data, and prints a grid that reveals a secret message made of uppercase letters.

How it works:
1. Fetches the published Google Doc HTML using the requests library with appropriate headers
2. Parses the HTML using BeautifulSoup to extract text content
3. Parses each line to extract character and (x, y) coordinates using string splitting
4. Creates a 2D grid based on the maximum x and y values, filled with spaces
5. Places each character at its specified (x, y) position in the grid
6. Prints the grid row by row to display the secret message

Requirements:
- Python 3.6+
- requests library: pip install requests
- beautifulsoup4 library: pip install beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup
import re


def decode_secret_message(url):
    """
    Takes a Google Doc URL, retrieves and parses the data,
    and prints the grid of characters forming a secret message.

    Args:
        url: String containing the URL for the Google Doc

    The function fetches the document, parses lines in the format "character x y",
    builds a 2D grid with the characters at their specified positions, and prints
    the grid to reveal uppercase letters forming the secret message.
    """
    # Fetch the published Google Doc content with headers to avoid blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the text content from the document
    text_content = soup.get_text()

    # Parse the data to extract character and coordinates
    coordinates = []

    # Split by lines and parse each line
    lines = text_content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Split the line into parts
        parts = line.split()

        if len(parts) >= 3:
            # Last two parts should be numbers (x, y coordinates)
            try:
                y = int(parts[-1])
                x = int(parts[-2])
                # Everything before the last two parts is the character
                char = ' '.join(parts[:-2])
                if char:  # Make sure we have a character
                    coordinates.append((char, x, y))
            except ValueError:
                # If conversion fails, this line doesn't match our pattern
                continue

    # Fallback: If no coordinates found, try regex pattern
    if not coordinates:
        pattern = r'(\S)\s+(\d+)\s+(\d+)'
        for match in re.finditer(pattern, text_content):
            char = match.group(1)
            x = int(match.group(2))
            y = int(match.group(3))
            coordinates.append((char, x, y))

    if not coordinates:
        print("Error: Could not parse any coordinates from the document")
        return

    # Determine grid dimensions based on maximum x and y coordinates
    max_x = max(coord[1] for coord in coordinates)
    max_y = max(coord[2] for coord in coordinates)

    # Create grid filled with spaces
    # Grid dimensions are (max_y + 1) rows and (max_x + 1) columns
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Place characters at their specified positions
    for char, x, y in coordinates:
        grid[y][x] = char

    # Print the grid row by row
    for row in grid:
        print(''.join(row))


if __name__ == "__main__":
    # URL for the Google Doc with the secret message
    url = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"

    print("Decoding secret message...")
    print()
    decode_secret_message(url)
