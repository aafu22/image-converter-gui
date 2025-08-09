import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def convert_png_to_jpg():
    # pick a PNG
    png_path = filedialog.askopenfilename(
        title="Select a PNG file",
        filetypes=[("PNG images", "*.png")]
    )
    if not png_path:
        return

    # suggest a JPG name
    default_name = os.path.splitext(os.path.basename(png_path))[0] + ".jpg"
    save_path = filedialog.asksaveasfilename(
        title="Save as JPG",
        defaultextension=".jpg",
        initialfile=default_name,
        filetypes=[("JPEG images", "*.jpg;*.jpeg")]
    )
    if not save_path:
        return

    # convert (handles transparency by placing over white)
    try:
        with Image.open(png_path) as im:
            if im.mode in ("RGBA", "LA"):
                bg = Image.new("RGB", im.size, (255, 255, 255))
                alpha = im.split()[-1]
                bg.paste(im, mask=alpha)
                bg.save(save_path, "JPEG", quality=95, optimize=True)
            else:
                im.convert("RGB").save(save_path, "JPEG", quality=95, optimize=True)
        messagebox.showinfo("Success", f"Saved:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed:\n{e}")

# ---- GUI ----
root = tk.Tk()
root.title("PNG → JPG Converter")
root.geometry("380x160")

tk.Label(root, text="Convert a PNG image to JPG", font=("Segoe UI", 11)).pack(pady=12)
tk.Button(root, text="Select PNG & Convert", command=convert_png_to_jpg, width=24).pack(pady=6)
tk.Label(root, text="Tip: transparent PNGs are flattened on white.").pack(pady=6)

root.mainloop()
