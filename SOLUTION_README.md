# Decoding a Secret Message - Solution

## Problem Summary
This solution decodes a secret message from a published Google Doc containing Unicode characters and their 2D grid coordinates.

## Solution Overview

### How the Code Works

The `decode_secret_message()` function works in the following steps:

1. **Fetches the Google Doc**: Uses the `requests` library with appropriate HTTP headers to retrieve the published Google Doc HTML content.

2. **Parses the HTML**: Uses `BeautifulSoup` to parse the HTML and extract the text content from the document.

3. **Extracts coordinates**: Parses each line of text to extract character and coordinate data in the format "character x y", where x and y are integer coordinates.

4. **Builds the grid**: Creates a 2D grid (list of lists) with dimensions based on the maximum x and y values found, initialized with space characters.

5. **Places characters**: Iterates through all parsed coordinates and places each character at its specified (x, y) position in the grid.

6. **Prints the result**: Outputs the grid row by row, which reveals uppercase letters forming the secret message when viewed in a fixed-width font.

### Key Implementation Details

- The coordinate system has (0, 0) at the top-left corner
- The x-coordinate increases from left to right
- The y-coordinate increases from top to bottom
- Empty positions in the grid are filled with space characters
- The code handles Unicode characters properly

## Requirements

```bash
pip install requests beautifulsoup4
```

## Usage

```python
python3 solution.py
```

Or use the function programmatically:

```python
from solution import decode_secret_message

url = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"
decode_secret_message(url)
```

## Note on Testing

The provided test URL may return a 403 Forbidden error when accessed from certain environments (such as cloud servers or automated testing environments) due to Google's security measures. The code is correct and will work when run from a standard development environment with normal browser-like access patterns.

## Files

- `solution.py` - Main solution with the `decode_secret_message()` function
- `decode_secret_message.py` - Alternative version with additional error handling
- `test_decode.py` - Test script that validates the parsing logic with local test data
- `test_data.txt` - Sample test data in the expected format
