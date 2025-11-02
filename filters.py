from PIL import Image, ImageTk
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import numpy as np

### ------ Filters


# Convert image to black and white - returns PIL img
def apply_black_and_white(img):
    return img.convert("L")


# Convert image to sepia - returns PIL img
def apply_sepia(img, intensity=1.0):
    if img.mode != "RGB":
        img = img.convert("RGB")

    np_img = np.array(img, dtype=np.float32)

    sepia_matrix = np.array(
        [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
    )

    sepia = np_img @ sepia_matrix.T
    sepia = np.clip(sepia, 0, 255)

    result = (np_img * (1 - intensity) + sepia * intensity).astype(np.uint8)
    sepia_img = Image.fromarray(result)

    scale = 0.4 * intensity
    sepia_img = adjust_contrast(sepia_img, scale=scale)

    return sepia_img


# Apply contrast on the image - returns PIL img
def adjust_contrast(img, scale=0.0):
    if img.mode != "RGB":
        img = img.convert("RGB")

    np_img = np.array(img, dtype=np.float32)

    factor = 1.0 + scale

    midpoint = 127.5
    np_img = (np_img - midpoint) * factor + midpoint
    np_img = np.clip(np_img, 0, 255).astype(np.uint8)

    return Image.fromarray(np_img)


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
