from pathlib import Path
import sys
from filters import (
    load_image,
    apply_black_and_white,
    apply_sepia,
    show_image,
    pick_image_file,
    pick_output_folder,
)
from grids import compute_axis, draw_grid
import tkinter as tk


# Pick an image file, apply filters, show previews, and save results.
def test_filters_interactive():
    try:
        image_path = pick_image_file()
        if not image_path:
            print("No image selected.")
            return

        img = load_image(image_path)
        print(f"✅ Loaded image: {image_path}")

        output_folder = pick_output_folder()
        if not output_folder:
            print("⚠️ No output folder selected, saving next to original image.")
            output_folder = Path(image_path).parent
        output_folder.mkdir(parents=True, exist_ok=True)
        print(f"Saving filtered images to: {output_folder}")

        ## -------- Test filters

        filters = [
            ("Black & White", apply_black_and_white, "_bw"),
            ("Sepia", apply_sepia, "_sepia"),
        ]

        for name, func, suffix in filters:
            print(f"Performing action {name} ...")
            filtered_img = func(img)
            show_image(filtered_img, title=name)

            out_path = (
                output_folder
                / f"{Path(image_path).stem}{suffix}{Path(image_path).suffix}"
            )
            filtered_img.save(out_path)
            print(f"✅ Files saved under: {out_path}")

        print("\n✅ All actions performed successfully.")

        ### -------- Test grids

        # center_x, center_y = compute_axis(img)
        # print(f"Axis at center: ({center_x}, {center_y})")

        print(f"Creating grid...")
        transformed_img = draw_grid(
            img, start="center", cols=4, rows=4, line_color=(255, 0, 0), line_width=2
        )
        show_image(transformed_img, title="Grid")
        out_path = (
            output_folder
            # / f"{Path(image_path).stem}{suffix}{Path(image_path).suffix}"
            / f"{Path(image_path).stem}_grid{Path(image_path).suffix}"
        )
        transformed_img.save(out_path)
        print(f"✅ Files saved under: {out_path}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


# Fallback version for running without file picker.
def test_filters_terminal(default_path="./images/input/landscape.jpg"):
    try:
        img = load_image(default_path)
        print(f"✅ Loaded image: {default_path}")

        filters = [
            ("Black & White", apply_black_and_white, "_bw"),
            ("Sepia", apply_sepia, "_sepia"),
        ]

        for name, func, suffix in filters:
            print(f"Applying {name} filter...")
            filtered_img = func(img)
            show_image(filtered_img, title=name)

            out_path = Path(default_path).with_name(
                f"{Path(default_path).stem}{suffix}{Path(default_path).suffix}"
            )
            filtered_img.save(out_path)
            print(f"✅ Saved: {out_path}")

        print("\n✅ All filters applied successfully.")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        test_filters_interactive()
    except tk.TclError:
        # In case running on a headless system (no display)
        print("⚠️ GUI not available, running terminal test instead.")
        test_filters_terminal()
