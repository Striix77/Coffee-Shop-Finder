import math
import sys
import urllib.request
import csv


# Fetch and parse the shop data from the given URL, returning a list of (name, x, y) tuples.
def fetch_and_parse(url):
    # Fetch the data from the URL and split it into lines.
    # The context manager ensures the response is always closed.
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8').splitlines()
    except Exception as e:
        error_exit(f"Error fetching shop data: {e}")

    # I used csv.reader because the input is expected to be comma‑separated text with three fields 
    # per line [ Name,Y Coordinate,X Coordinate ]. It safely handles edge cases like quoted values 
    # and commas inside names.
    reader = csv.reader(data)
    shops = []

    # Convert each row into (name, distance) and collect them.
    for row in reader:
        if len(row) != 3:
            error_exit("Each line in the shop data must have exactly 3 values: name, x coordinate, y coordinate.")

        name = row[0].strip()

        # Parse coordinates and throw error if they are invalid.
        try:
            shop_x = float(row[1].strip())
            shop_y = float(row[2].strip())
        except ValueError:
            error_exit("Invalid coordinates in row: " + ",".join(row))
        shops.append((name, shop_x, shop_y))
    
    return shops


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


# Print an error message to stderr and exit with non-zero status.
def error_exit(message):
    print(message, file=sys.stderr)
    exit(1)