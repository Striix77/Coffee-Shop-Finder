import math
import sys
import urllib.request
import csv


# Calculate Euclidean distance between two 2D points.
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Print an error message to stderr and exit with non-zero status.
def error_exit(message):
    print(message, file=sys.stderr)
    exit(1)

def main():
    if len(sys.argv) != 4:
        error_exit("Usage: python closest_coffee_shop.py <user x coordinate> <user y coordinate> <shop data url>")

    # Parse the user-provided coordinates as floats.
    try:
        user_x = float(sys.argv[1])
        user_y = float(sys.argv[2])
    except ValueError:
        error_exit("User coordinates must be valid float numbers.")

    # Third argument is a URL that points to the data.
    shop_data_url = sys.argv[3]

    # Fetch the data from the URL and split it into lines.
    # The context manager ensures the response is always closed.
    try:
        with urllib.request.urlopen(shop_data_url) as response:
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

        # Calculate distance from the user to this shop.
        dist = distance(user_x, user_y, shop_x, shop_y)

        # Store tuple of (name, distance) for later sorting.
        shops.append((name, dist))

    # Sort by the second tuple element (distance), ascending.
    shops.sort(key=lambda x: x[1])
    closest_shops = shops[:3]
    
    for shop in closest_shops:
        print(f"{shop[0]}: {shop[1]:.4f}")
        
        
if __name__ == "__main__":
    main()
    