import sys
from logic import fetch_and_parse, calculate_closest_shops, error_exit


def main():
    if len(sys.argv) != 4:
        error_exit("Usage: python closest_coffee_shop.py <user x coordinate> <user y coordinate> <shop data url>")

    # Parse the user-provided coordinates as floats.
    try:
        user_x = float(sys.argv[1])
        user_y = float(sys.argv[2])
    except ValueError:
        error_exit("User coordinates must be valid float numbers.")

    shop_data_url = sys.argv[3]

    shops = fetch_and_parse(shop_data_url)
    closest_shops = calculate_closest_shops(user_x, user_y, shops)
    
    for shop in closest_shops:
        print(f"{shop[0]}: {shop[1]:.4f}")
        
        
if __name__ == "__main__":
    main()
    