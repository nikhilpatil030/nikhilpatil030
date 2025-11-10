import requests
from bs4 import BeautifulSoup
import re


def decode_secret_message(url):
    """
    Takes a Google Doc URL, retrieves and parses the data,
    and prints the grid of characters forming a secret message.

    Args:
        url: String containing the URL for the Google Doc
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
        print("Note: This may occur if Google Docs is blocking automated requests from this environment.")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    coordinates = []

    # Method 1: Try to parse HTML table directly
    # Google Docs tables have structure: <table><tbody><tr><td>value</td>...</tr></tbody></table>
    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                try:
                    # Table format: x-coordinate, Character, y-coordinate
                    x = int(cells[0].get_text().strip())
                    char = cells[1].get_text().strip()
                    y = int(cells[2].get_text().strip())
                    if char:  # Make sure we have a character
                        coordinates.append((char, x, y))
                except (ValueError, IndexError):
                    continue

    # Method 2: If table parsing didn't work, try regex on text content
    # Pattern: number + character + number (concatenated like "27█0")
    if not coordinates:
        text_content = soup.get_text()
        pattern = r'(\d+)([█░▀▄▌▐▒▓■])(\d+)'
        for match in re.finditer(pattern, text_content):
            x = int(match.group(1))
            char = match.group(2)
            y = int(match.group(3))
            coordinates.append((char, x, y))

    # Method 3: Try space-separated format as final fallback
    if not coordinates:
        text_content = soup.get_text()
        lines = text_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 3:
                try:
                    y = int(parts[-1])
                    x = int(parts[-2])
                    char = ' '.join(parts[:-2])
                    if char:
                        coordinates.append((char, x, y))
                except ValueError:
                    continue

    if not coordinates:
        print("Error: Could not parse any coordinates from the document")
        print("Document text preview:")
        print(text_content[:500])
        return

    # Determine grid dimensions
    max_x = max(coord[1] for coord in coordinates)
    max_y = max(coord[2] for coord in coordinates)

    # Create grid filled with spaces
    # Grid dimensions are (max_y + 1) rows and (max_x + 1) columns
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Place characters at their specified positions
    for char, x, y in coordinates:
        grid[y][x] = char

    # Print the grid
    for row in grid:
        print(''.join(row))


if __name__ == "__main__":
    # Test with the provided URL
    test_url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"

    print("Decoding secret message from:", test_url)
    print("\nSecret message:")
    print("-" * 80)
    decode_secret_message(test_url)
    print("-" * 80)
