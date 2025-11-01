from PIL import Image, ImageTk
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

### ------ Filters


# Convert image to black and white - returns PIL img
def apply_black_and_white(img):
    return img.convert("L")


# Convert image to sepia - returns PIL img
def apply_sepia(img):
    sepia_img = img.convert("RGB")
    width, height = sepia_img.size
    pixels = sepia_img.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))
    return sepia_img


### ------ Utility Functions


# Load Image - returns PIL img
def load_image(path_str):
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    try:
        return Image.open(path)
    except Exception as e:
        raise IOError(f"Could not open image: {e}") from e


# Save Image - returns file path where the saved image is written
def save_image(path, suffix, output_dir=None):
    img = load_image(path)
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = output_dir / f"{path.stem}{suffix}{path.suffix}"
    else:
        out_file = path.with_name(f"{path.stem}{suffix}{path.suffix}")

    img.save(out_file)
    print(f"Saved filtered image to: {out_file}")
    return out_file


# Show Image - does not return anything; it displays a PIL image in a Tkinter window
def show_image(img, title="Image"):
    root = tk.Tk()
    root.title(title)
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=tk_img)
    label.pack()
    root.mainloop()


# Pick Image - returns picked file path
def pick_image_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif")],
    )
    root.destroy()
    return file_path if file_path else None


def pick_output_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title="Select Output Folder")
    folder_path = folder_path.strip() if folder_path else ""
    root.destroy()
    return Path(folder_path) if folder_path else None
