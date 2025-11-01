from PIL import Image, ImageDraw
from typing import Tuple, Optional


# Finds center of an image - returns the (x, y) coordinates of the center of the image.
def find_center(img: Image.Image) -> Tuple[int, int]:
    width, height = img.size
    center_x = width // 2
    center_y = height // 2
    return center_x, center_y


# Computes main axis of an image - returns the (x, y) coordinates. If none specified, finds center.
# def compute_axis(img, central_x=None, central_y=None):
#     width, height = img.size
#     center_x = central_x if central_x is not None else width // 2
#     center_y = central_y if central_y is not None else height // 2
#     return center_x, center_y


# Computes main axis of an image - returns the (x, y) coordinates. If none specified, finds center as tuple.
def compute_axis(
    img: Image.Image, central_x: Optional[int] = None, central_y: Optional[int] = None
) -> Tuple[int, int]:
    width, height = img.size

    center_x = central_x if central_x is not None else width // 2
    center_y = central_y if central_y is not None else height // 2

    return center_x, center_y


def determine_starting_point(
    start: str, img_width: int, img_height: int
) -> tuple[int, int]:
    match start:
        case "center":
            x0 = img_width // 2
            y0 = img_height // 2
        case "left":
            x0 = 0
            y0 = 0
        case "right":
            x0 = img_width
            y0 = 0
        case _:
            raise ValueError("start must be 'center', 'left', or 'right'")
    return x0, y0


def compute_positions(
    total_size: int,
    count: Optional[int] = None,
    spacing: Optional[int] = None,
) -> Tuple[int, list]:
    if count is None and spacing is None:
        # Default: single line in middle
        count = 1
        segment_size = total_size
        positions = [0]
    elif count is not None and spacing is None:
        # Count specified, spacing not
        if count == 1:
            segment_size = total_size
            positions = [0]
        else:
            segment_size = total_size // count
            positions = [i * segment_size for i in range(count)]
    elif spacing is not None and count is None:
        # Spacing specified, compute count
        count = max(1, total_size // spacing)
        segment_size = total_size // count
        positions = [i * segment_size for i in range(count)]
    else:
        # Both count and spacing specified
        segment_size = spacing
        positions = [i * spacing for i in range(count)]

    return segment_size, positions


def draw_grid(
    img: Image.Image,
    start: str = "center",  # 'center', 'left', 'right'
    rows: Optional[int] = None,
    cols: Optional[int] = None,
    row_spacing: Optional[int] = None,
    col_spacing: Optional[int] = None,
    line_color: Tuple[int, int, int] = (0, 0, 255),  # Blue
    line_width: int = 2,
) -> Image.Image:

    img_copy = img.copy()
    draw = ImageDraw.Draw(img_copy)
    width, height = img_copy.size

    x_offset, y_offset = determine_starting_point(start, width, height)

    # Compute column and row positions
    _, x_positions = compute_positions(width, cols, col_spacing)
    _, y_positions = compute_positions(height, rows, row_spacing)

    # Apply offset to positions if start is not 'left'
    x_positions = [
        (
            x - width // 2 + x_offset
            if start == "center"
            else x + x_offset if start == "right" else x
        )
        for x in x_positions
    ]
    y_positions = [
        (
            y - height // 2 + y_offset
            if start == "center"
            else y + y_offset if start == "right" else y
        )
        for y in y_positions
    ]

    # Draw vertical lines
    for x in x_positions:
        draw.line([(x, 0), (x, height)], fill=line_color, width=line_width)

    # Draw horizontal lines
    for y in y_positions:
        draw.line([(0, y), (width, y)], fill=line_color, width=line_width)

    return img_copy
