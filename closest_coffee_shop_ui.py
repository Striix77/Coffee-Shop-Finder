import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from logic import fetch_and_parse_url, parse_file, parse_text, calculate_closest_shops


def find_shops():
    # Read values from the input fields and convert coordinates to floats.
    try:
        user_x = float(entry_x.get())
        user_y = float(entry_y.get())
    except ValueError:
        # Coordinate parsing failed (empty or non-numeric input).
        messagebox.showerror("Error", "Invalid coordinates.")
        return

    # Determine the source type and fetch/parse the shop data accordingly.
    source_type = source_var.get()
    try:
        if source_type == "url":
            url = entry_url.get().strip()
            shops = fetch_and_parse_url(url)
        elif source_type == "file":
            path = entry_url.get().strip()
            shops = parse_file(path)
        else:
            text = entry_text.get("1.0", tk.END)
            shops = parse_text(text)
    except Exception as e:
        # Show network or parsing errors in a user-friendly dialog.
        messagebox.showerror("Error", f"Failed to fetch shop data: {e}")
        return

    # Calculate closest shops to the user's location using shared logic.
    closest_shops = calculate_closest_shops(user_x, user_y, shops)

    # Clear previous results, then render the new ones line by line.
    output.configure(state=tk.NORMAL)
    output.delete(1.0, tk.END)
    for shop in closest_shops:
        output.insert(tk.END, f"{shop[0]}: {shop[1]:.4f}\n")
    output.configure(state=tk.DISABLED)


root = tk.Tk()
root.title("Closest Coffee Shop Finder")
root.minsize(600, 400)

style = ttk.Style()
style.theme_use("xpnative")

ttk.Label(root, text="User X Coordinate:").grid(row=0, column=0, sticky="e")
entry_x = ttk.Entry(root)
entry_x.grid(row=0, column=1)

ttk.Label(root, text="User Y Coordinate:").grid(row=1, column=0, sticky="e")
entry_y = ttk.Entry(root)
entry_y.grid(row=1, column=1)

ttk.Label(root, text="Data Source:").grid(row=2, column=0, sticky="ne")

source_var = tk.StringVar(value="url")

# Function to update the UI based on the selected data source type.
def update_source_ui():
    source_type = source_var.get()
    if source_type == "text":
        entry_text_label.grid(row=4, column=0, sticky="ne")
        entry_text.grid(row=4, column=1, padx=10, pady=5)
        entry_url.grid_remove()
        browse_button.grid_remove()

    elif source_type == "file":
        entry_url.grid(row=3, column=1, sticky="w")
        entry_url.delete(0, tk.END)
        browse_button.grid(row=3, column=0, sticky="e")
        entry_text.grid_remove()
        entry_text_label.grid_remove()
    else:
        entry_url.grid(row=3, column=1, sticky="w")
        entry_url.delete(0, tk.END)
        browse_button.grid_remove()
        entry_text.grid_remove()
        entry_text_label.grid_remove()
        

source_frame = ttk.Frame(root)
source_frame.grid(row=2, column=1, sticky="w")
ttk.Radiobutton(source_frame, text="URL", variable=source_var, value="url", command=update_source_ui).grid(row=0, column=0, sticky="w")
ttk.Radiobutton(source_frame, text="File", variable=source_var, value="file", command=update_source_ui).grid(row=0, column=1, sticky="w")
ttk.Radiobutton(source_frame, text="Text", variable=source_var, value="text", command=update_source_ui).grid(row=0, column=2, sticky="w")

entry_url = ttk.Entry(root, width=50)
entry_url.grid(row=3, column=1, sticky="w")

# Helper function to open a file dialog and populate the file path entry.
def choose_file():
    path = filedialog.askopenfilename(
        title="Select shop data file",
        filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")],
    )
    if path:
        entry_url.delete(0, tk.END)
        entry_url.insert(0, path)

browse_button = ttk.Button(root, text="Browse...", command=choose_file)
browse_button.grid(row=3, column=0, sticky="e")

entry_text_label = ttk.Label(root, text="Raw Text:")
entry_text_label.grid(row=4, column=0, sticky="ne")
entry_text = tk.Text(root, height=6, width=60)
entry_text.grid(row=4, column=1, padx=10, pady=5)

update_source_ui()

btn = ttk.Button(root, text="Find Closest Coffee Shops", command=find_shops)
btn.grid(row=5, column=0, columnspan=2, pady=5)

output = tk.Text(root, height=6, width=60, font=("TkDefaultFont", 10), relief="flat")
output.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
output.configure(state=tk.DISABLED)


root.mainloop()