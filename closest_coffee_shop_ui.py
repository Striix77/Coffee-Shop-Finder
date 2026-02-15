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
root.minsize(750,600)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.option_add("*Font", "Helvetica 14")



style = ttk.Style()
style.theme_use("xpnative")
style.configure("Large.TRadiobutton", font=("Helvetica", 14))
style.configure("Large.TButton", font=("Helvetica", 14))

wrapper = ttk.Frame(root)
wrapper.grid(row=0, column=0, sticky="nsew")
wrapper.grid_rowconfigure(0, weight=1)
wrapper.grid_columnconfigure(0, weight=1)

main_frame = ttk.Frame(wrapper, padding="20")
main_frame.grid(row=0, column=0)
main_frame.grid_columnconfigure(0, weight=1)


header_frame = ttk.Frame(main_frame)
header_frame.grid(row=0, column=0, pady=(0, 20))

title_label = ttk.Label(header_frame, text="Coffee Shop Finder", font=("Helvetica", 24, "bold"))
title_label.grid(row=0, column=0)

subtitle_label = ttk.Label(header_frame, text="Find the closest coffee shops to your location", font=("Helvetica", 12))
subtitle_label.grid(row=1, column=0, pady=(5, 0))

input_frame = ttk.Frame(main_frame)
input_frame.grid(row=1, column=0, pady=10)
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=1)

ttk.Label(input_frame, text="User X Coordinate:").grid(row=0, column=0,pady=5,padx=5)
entry_x = ttk.Entry(input_frame,width=25)
entry_x.grid(row=0, column=1,pady=5)

ttk.Label(input_frame, text="User Y Coordinate:").grid(row=1, column=0,pady=5,padx=5)
entry_y = ttk.Entry(input_frame,width=25)
entry_y.grid(row=1, column=1,pady=5)

ttk.Label(input_frame, text="Data Source:").grid(row=4, column=0,pady=10)

source_var = tk.StringVar(value="url")

# Function to update the UI based on the selected data source type.
def update_source_ui():
    for widget in dynamic_frame.winfo_children():
        widget.grid_forget()
    source_type = source_var.get()
    if source_type in ("url", "file"):
        entry_url.grid(row=0, column=0, padx=5, pady=1)
        if source_type == "file":
            browse_button.grid(row=0, column=1, padx=5, pady=1,ipady=2)
    else:
        entry_text.grid(row=0, column=0, padx=5, pady=1)
        

source_frame = ttk.Frame(input_frame)
source_frame.grid(row=4, column=1,pady=5)
ttk.Radiobutton(source_frame, text="URL", variable=source_var, value="url", command=update_source_ui,style="Large.TRadiobutton").grid(row=0, column=0, sticky="w")
ttk.Radiobutton(source_frame, text="File", variable=source_var, value="file", command=update_source_ui,style="Large.TRadiobutton").grid(row=0, column=1, sticky="w")
ttk.Radiobutton(source_frame, text="Text", variable=source_var, value="text", command=update_source_ui,style="Large.TRadiobutton").grid(row=0, column=2, sticky="w")

dynamic_frame = ttk.Frame(main_frame)
dynamic_frame.grid(row=2, column=0, pady=1)
dynamic_frame.grid_columnconfigure(0, weight=1)

entry_url = ttk.Entry(dynamic_frame, width=50)
entry_url.grid(row=0, column=0, padx=5, pady=1)


# Helper function to open a file dialog and populate the file path entry.
def choose_file():
    path = filedialog.askopenfilename(
        title="Select shop data file",
        filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")],
    )
    if path:
        entry_url.delete(0, tk.END)
        entry_url.insert(0, path)

browse_button = ttk.Button(dynamic_frame, text="Browse...", command=choose_file, style="Large.TButton")
browse_button.grid(row=0, column=1, padx=5, pady=1,ipady=2)

entry_text = tk.Text(dynamic_frame, height=6, width=60)
entry_text.grid(row=0, column=0, padx=5, pady=1)


update_source_ui()

btn = ttk.Button(main_frame, text="Find Closest Coffee Shops", command=find_shops, style="Large.TButton")
btn.grid(row=3, column=0,ipadx=5,ipady=2,pady=10)

output = tk.Text(main_frame, height=6, width=60, font=("Helvetica", 14), relief="flat" )
output.grid(row=4, column=0,padx=10, pady=5)
output.configure(state=tk.DISABLED)


root.mainloop()