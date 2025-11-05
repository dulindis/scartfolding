from io import BytesIO
from PIL import Image, ImageTk
from pathlib import Path

### ------ Utility Functions

# Load Image - returns PIL img
def load_image(source):
    if isinstance(source, (str, Path)):
        return Image.open(source)
    elif hasattr(source, "read"):  # file-like (like from st.file_uploader)
        return Image.open(source)
    else:
        raise TypeError("Unsupported source type for load_image")


def image_to_bytes(img, format="PNG"):

    buf = BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


# ### functionality  for thinker - TK
# # Save Image - returns file path where the saved image is written - for TK
# def save_image(path, suffix, output_dir=None):
#     img = load_image(path)
#     path = Path(path)

#     if not path.exists():
#         raise FileNotFoundError(f"Image not found: {path}")

#     if output_dir:
#         output_dir = Path(output_dir)
#         output_dir.mkdir(parents=True, exist_ok=True)
#         out_file = output_dir / f"{path.stem}{suffix}{path.suffix}"
#     else:
#         out_file = path.with_name(f"{path.stem}{suffix}{path.suffix}")

#     img.save(out_file)
#     print(f"Saved filtered image to: {out_file}")
#     img.close()
#     return out_file

# # # Load Image - returns PIL img - for TK
# # def load_image(path_str):
# #     path = Path(path_str)
# #     if not path.exists():
# #         raise FileNotFoundError(f"Image not found: {path}")
# #     try:
# #         img = Image.open(path_str)
# #         return img
# #     except Exception as e:
# #         raise IOError(f"Could not open image: {e}") from e


# # Show Image - does not return anything; it displays a PIL image in a Tkinter window  - for TK
# def show_image(img, title="Image"):
#     root = tk.Tk()
#     root.title(title)

#     tk_img = ImageTk.PhotoImage(img.copy())
#     label = tk.Label(root, image=tk_img)
#     label.image = tk_img
#     label.pack()

#     root.mainloop()

# # Pick Image - returns picked file path  - for TK
# def pick_image_file():
#     root = tk.Tk()
#     root.withdraw()
#     file_path = filedialog.askopenfilename(
#         title="Select an image",
#         filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif")],
#     )
#     root.destroy()
#     return file_path if file_path else None

# # Pick Folder - returns picked directory path  - for TK
# def pick_output_folder():
#     root = tk.Tk()
#     root.withdraw()  # Hide the main window
#     folder_path = filedialog.askdirectory(title="Select Output Folder")
#     folder_path = folder_path.strip() if folder_path else ""
#     root.destroy()
#     return Path(folder_path) if folder_path else None
