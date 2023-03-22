import tkinter as tk
from tkinter import ttk
import qrcode
from PIL import ImageTk, Image
import os


def generate_urls():
    unique_id = uuid_entry.get()
    table_numbers_input = table_numbers_entry.get().replace(" ", "")

    if "-" in table_numbers_input:
        start, end = map(int, table_numbers_input.split("-"))
        table_numbers = list(range(start, end + 1))
    else:
        table_numbers = table_numbers_input.split(",")

    urls = []
    for num in table_numbers:
        url = f"https://getunion.com/app?venue_uuid={unique_id}&table_name={num}"
        urls.append(url)

    output.delete(1.0, tk.END)
    output.insert(tk.END, "\n".join(urls))

    return urls

def generate_qr_codes():
    venue_name = venue_name_entry.get().lower()
    urls = output.get(1.0, tk.END).strip().split("\n")
    qr_color = qr_color_var.get()

    if venue_name and urls:
        os.makedirs(venue_name, exist_ok=True)

        for url in urls:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color=qr_color, back_color="transparent" if qr_color == "white" else "white", image_factory=None).convert('RGBA')
            img = img.resize((1000, 1000), Image.ANTIALIAS)
            file_name = f"{venue_name}/{url.split('=')[-1]}_{venue_name}.png"
            img.save(file_name)

class CustomButton(tk.Canvas):
    def __init__(self, parent, text, command, font, bg, fg, width, height, *args, **kwargs):
        tk.Canvas.__init__(self, parent, width=width, height=height, *args, **kwargs)
        self.config(highlightthickness=0, background=bg, bd=0)
        self.bind("<Button-1>", lambda event: command())
        self.create_rectangle(0, 0, width, height, outline=bg, fill=bg)
        self.create_text(width // 2, height // 2, text=text, font=font, fill=fg)

root = tk.Tk()
root.title("Location Marker Generator")
root.configure(bg="#fafafa")

# Custom fonts and colors
heading_font = ("PP Neue Montreal", 31, "bold")
label_font = ("Arial", 14)
entry_font = ("Arial", 13)
button_font = ("Arial", 14, "bold")
button_bg = "black"
button_fg = "white"

# Create heading
heading = tk.Label(root, text="Location Marker Generator", font=heading_font, bg="#fafafa")
heading.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

# Create labels
venue_name_label = tk.Label(root, text="Venue Name:", font=label_font, bg="#fafafa", anchor="w", width=13)
venue_name_label.grid(row=1, column=0, padx=(20, 0), pady=10, sticky="w")
uuid_label = tk.Label(root, text="UUID:", font=label_font, bg="#fafafa", anchor="w", width=13)
uuid_label.grid(row=2, column=0, padx=(20, 0), pady=10, sticky="w")
table_numbers_label = tk.Label(root, text="Table Numbers:", font=label_font, bg="#fafafa", anchor="w", width=13)
table_numbers_label.grid(row=3, column=0, padx=(20, 0), pady=10, sticky="w")
qr_color_label = tk.Label(root, text="QR Code Color:", font=label_font, bg="#fafafa", anchor="w")
qr_color_label.grid(row=4, column=0, padx=(20, 0), pady=10, sticky="w")

# Create entry fields
venue_name_entry = tk.Entry(root, font=entry_font)
venue_name_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="w")
uuid_entry = tk.Entry(root, font=entry_font)
uuid_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="w")
table_numbers_entry = tk.Entry(root, font=entry_font)
table_numbers_entry.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="w")

# Create QR color toggle
qr_color_var = tk.StringVar()
qr_color_var.set("black")
qr_color_combobox = ttk.Combobox(root, textvariable=qr_color_var, values=("black", "white"), state="readonly", font=entry_font, width=10)
qr_color_combobox.grid(row=4, column=1, padx=(0, 20), pady=10, sticky="w")

# Create button frames
top_button_frame = tk.Frame(root, bg="#fafafa")
top_button_frame.grid(row=4, column=0, padx=(20, 0), pady=10, sticky="w")
bottom_button_frame = tk.Frame(root, bg="#fafafa")
bottom_button_frame.grid(row=6, column=0, padx=(20, 0), pady=10, sticky="w")


# Create buttons
generate_button = CustomButton(top_button_frame, text="1. Generate URLs", command=generate_urls, font=button_font, bg=button_bg, fg=button_fg, width=180, height=30)
generate_button.pack()
generate_qr_button = CustomButton(bottom_button_frame, text="2. Generate QR Codes", command=generate_qr_codes, font=button_font, bg=button_bg, fg=button_fg, width=180, height=30)
generate_qr_button.pack()

# Create output
output = tk.Text(root, wrap="word", height=10, width=60)
output.grid(row=7, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="w")


root.mainloop()