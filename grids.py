from typing import Tuple, Optional
from enum import Enum
import numpy as np
import cv2
from utils import to_uint8_rgb, to_rgba


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


# Draws grid over an image  -returns np array  -gets 32 and terutns 32
def draw_grid(
    img: np.ndarray,
    start: GridStart = GridStart.CENTER,
    rows: Optional[int] = 3,
    cols: Optional[int] = 3,
    row_spacing: Optional[int] = None,
    col_spacing: Optional[int] = None,
    line_color: Tuple[int, int, int] = (255, 0, 0),
    line_width: int = 2,
    draw_frame: bool = True,
) -> np.ndarray:

    img_copy = img.copy()
    img_rgb = to_uint8_rgb(img_copy)
    height, width = img_copy.shape[:2]

    # Convert RGB -> BGR for OpenCV
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    line_color_bgr = (line_color[2], line_color[1], line_color[0])  # RGB -> BGR

    # Calculate line positions
    x_positions, y_positions = compute_grid_positions(
        width, height, cols, rows, col_spacing, row_spacing, start
    )

    # Draw vertical and horizontal grid lines
    for x in x_positions:
        cv2.line(
            # img_rgb,
            img_bgr,
            (int(round(x)), 0),
            (int(round(x)), height),
            # color=line_color,
            color=line_color_bgr,
            thickness=line_width,
        )
    for y in y_positions:
        cv2.line(
            # img_rgb,
            img_bgr,
            (0, int(round(y))),
            (width, int(round(y))),
            # color=line_color,
            color=line_color_bgr,
            thickness=line_width,
        )

    # Optional frame
    if draw_frame:
        cv2.rectangle(
            # img_rgb,
            img_bgr,
            (0, 0),
            (width - 1, height - 1),
            # color=line_color,
            color=line_color_bgr,
            thickness=line_width,
        )

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    if img_copy.shape[-1] == 4:
        img_grid = to_rgba(img_rgb)
    else:
        img_grid = img_rgb
    return img_grid


# TOFIX:Ah! That OpenCV error is happening because cv2.line does not accept float32 arrays. It only works with uint8 (0–255) or int arrays. In your draw_grid, to_rgb(img_copy) is returning float32 (because your pipeline uses float32 for processing), so OpenCV cannot draw lines on it.
