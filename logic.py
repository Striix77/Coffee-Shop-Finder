import math
import sys
import urllib.request
import csv

# Print an error message to stderr and exit with non-zero status.
def error_exit(message):
    print(message, file=sys.stderr)
    exit(1)

def parse_shop_data(text):
    # Parse comma-separated text into a list of (name, x, y) tuples.
    data = text.splitlines()
    reader = csv.reader(data)
    shops = []

    for row in reader:
        if len(row) != 3:
            error_exit("Each line in the shop data must have exactly 3 values: name, x coordinate, y coordinate.")

        name = row[0].strip()
        try:
            shop_x = float(row[1].strip())
            shop_y = float(row[2].strip())
        except ValueError:
            error_exit("Invalid coordinates in row: " + ",".join(row))

        shops.append((name, shop_x, shop_y))

    return shops


def fetch_and_parse_url(url):
    # Fetch the data from the URL and parse it as comma-separated text.
    try:
        with urllib.request.urlopen(url) as response:
            text = response.read().decode("utf-8")
    except Exception as e:
        error_exit(f"Error fetching shop data: {e}")

    return parse_shop_data(text)


def parse_file(path):
    # Read file contents and parse as comma-separated text.
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        error_exit(f"Error reading shop data file: {e}")

    return parse_shop_data(text)


def parse_text(text):
    # Parse raw text as comma-separated input.
    return parse_shop_data(text)


# Backward-compatible helper used by the CLI.
def fetch_and_parse(url):
    return fetch_and_parse_url(url)


# Calculate Euclidean distance between two 2D points.
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Calculate the closest shops to the user and return a list of (name, distance) tuples for the n closest shops.
def calculate_closest_shops(user_x, user_y, shops, n=3):
    closest_shops = []
    for name, shop_x, shop_y in shops:
        dist = distance(user_x, user_y, shop_x, shop_y)
        closest_shops.append((name, dist))

    # Sort by the second tuple element (distance), ascending.
    closest_shops.sort(key=lambda x: x[1])
    return closest_shops[:n]


