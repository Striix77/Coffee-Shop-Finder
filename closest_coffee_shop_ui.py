import tkinter as tk
from tkinter import messagebox
from logic import fetch_and_parse, calculate_closest_shops, error_exit


def find_shops():
    # Read values from the input fields and convert coordinates to floats.
    try:
        user_x = float(entry_x.get())
        user_y = float(entry_y.get())
        url = entry_url.get()
    except ValueError:
        # Coordinate parsing failed (empty or non-numeric input).
        messagebox.showerror("Error", "Invalid coordinates.")
        return

    # Download and parse the shop data from the URL.
    try:
        shops = fetch_and_parse(url)
    except Exception as e:
        # Show network or parsing errors in a user-friendly dialog.
        messagebox.showerror("Error", f"Failed to fetch shop data: {e}")
        return

    # Calculate closest shops to the user's location using shared logic.
    closest_shops = calculate_closest_shops(user_x, user_y, shops)

    # Clear previous results, then render the new ones line by line.
    output.delete(1.0, tk.END)
    for shop in closest_shops:
        output.insert(tk.END, f"{shop[0]}: {shop[1]:.4f}\n")


root = tk.Tk()
root.title("Closest Coffee Shop Finder")

tk.Label(root, text="User X Coordinate:").grid(row=0, column=0, sticky="e")
entry_x = tk.Entry(root)
entry_x.grid(row=0, column=1)

tk.Label(root, text="User Y Coordinate:").grid(row=1, column=0, sticky="e")
entry_y = tk.Entry(root)
entry_y.grid(row=1, column=1)

tk.Label(root, text="CSV URL:").grid(row=2, column=0, sticky="e")
entry_url = tk.Entry(root, width=50)
entry_url.grid(row=2, column=1)

btn = tk.Button(root, text="Find Closest Coffee Shops", command=find_shops)
btn.grid(row=3, column=0, columnspan=2, pady=5)

output = tk.Text(root, height=6, width=60)
output.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


root.mainloop()