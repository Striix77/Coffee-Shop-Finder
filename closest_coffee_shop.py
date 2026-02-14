import math
import sys
import urllib.request
import csv


def distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def error_exit(message):
    print(message, file=sys.stderr)
    exit(1)

def main():
    if len(sys.argv) != 4:
        error_exit("Usage: python closest_coffee_shop.py <user x coordinate> <user y coordinate> <shop data url>")
    
    try:
        user_x = float(sys.argv[1])
        user_y = float(sys.argv[2])
    except ValueError:
        error_exit("User coordinates must be valid numbers.")
        
    shop_data_url = sys.argv[3]
    
    try:
        with urllib.request.urlopen(shop_data_url) as response:
            data = response.read().decode('utf-8').splitlines()
    except Exception as e:
        error_exit(f"Error fetching shop data: {e}")
    
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
        dist = distance(user_x, user_y, shop_x, shop_y)
        shops.append((name, dist))
    
    shops.sort(key=lambda x: x[1])
    closest_shops = shops[:3]
    
    for shop in closest_shops:
        print(f"{shop[0]}: {shop[1]:.4f}")
        
        
if __name__ == "__main__":    
    main()
    