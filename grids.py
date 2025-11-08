from PIL import Image, ImageDraw
from typing import Tuple, Optional
from enum import Enum

### ------ Grids


class GridStart(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


# Computes positions of lines - returns a tuple
def compute_grid_positions(
    width: int,
    height: int,
    cols: Optional[int],
    rows: Optional[int],
    col_spacing: Optional[int],
    row_spacing: Optional[int],
    start: GridStart = GridStart.CENTER,
) -> Tuple[list[float], list[float]]:

    if cols and not col_spacing:
        col_spacing = width / cols
    if rows and not row_spacing:
        row_spacing = height / rows

    if not cols and col_spacing:
        cols = max(1, int(width // col_spacing))
    if not rows and row_spacing:
        rows = max(1, int(height // row_spacing))

    x_positions, y_positions = [], []

    if start == GridStart.CENTER:
        x_center, y_center = width / 2, height / 2

        if cols > 1:
            for i in range(-(cols // 2), (cols // 2) + 1):
                x = x_center + i * col_spacing
                if 0 <= x <= width:
                    x_positions.append(x)

        if rows > 1:
            for j in range(-(rows // 2), (rows // 2) + 1):
                y = y_center + j * row_spacing
                if 0 <= y <= height:
                    y_positions.append(y)

    elif start == GridStart.LEFT:
        x_positions = [i * col_spacing for i in range(1, cols)]
        y_positions = [j * row_spacing for j in range(1, rows)]

    elif start == GridStart.RIGHT:
        x_positions = [width - i * col_spacing for i in range(1, cols)]
        y_positions = [j * row_spacing for j in range(1, rows)]

    else:
        raise ValueError("Start must be a supported GridStart enum ")

    return x_positions, y_positions


# Draws grid over an image  -returns new PIL
def draw_grid(
    img: Image.Image,
    start: GridStart = GridStart.CENTER,
    rows: Optional[int] = 3,
    cols: Optional[int] = 3,
    row_spacing: Optional[int] = None,
    col_spacing: Optional[int] = None,
    line_color: Tuple[int, int, int] = (255, 0, 0),
    line_width: int = 2,
    draw_frame: bool = True,
) -> Image.Image:

    # if rows <= 1 and cols <= 1:
    #     return img.copy()

    if img.mode != "RGB":
        img_copy = img.convert("RGB")
    else:
        img_copy = img.copy()

    draw = ImageDraw.Draw(img_copy)
    width, height = img.size

    # Calculate line positions
    x_positions, y_positions = compute_grid_positions(
        width, height, cols, rows, col_spacing, row_spacing, start
    )

    # Draw vertical and horizontal grid lines
    for x in x_positions:
        draw.line([(x, 0), (x, height)], fill=line_color, width=line_width)
    for y in y_positions:
        draw.line([(0, y), (width, y)], fill=line_color, width=line_width)

    # Optional frame
    if draw_frame:
        draw.rectangle(
            [(0, 0), (width - 1, height - 1)], outline=line_color, width=line_width
        )

    return img_copy
