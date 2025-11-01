from PIL import Image, ImageDraw
# from typing import Tuple, Optional

# Finds center of an image - returns the (x, y) coordinates of the center of the image.
# def find_center(img: Image.Image) -> Tuple[int, int]:
#     width, height = img.size
#     center_x = width // 2
#     center_y = height // 2
#     return center_x, center_y

def compute_axis(img, central_x=None, central_y=None):
    width, height = img.size

    center_x = central_x if central_x is not None else width // 2
    center_y = central_y if central_y is not None else height // 2

    return center_x, center_y

# def compute_axis(
#     img: Image.Image,
#     central_x: Optional[int] = None,
#     central_y: Optional[int] = None
# ) -> Tuple[int, int]:
#     width, height = img.size

#     center_x = central_x if central_x is not None else width // 2
#     center_y = central_y if central_y is not None else height // 2
#     return center_x, center_y

#  Draws a vertical and horizontal line through the center of the image- Returns a new PIL image with the lines.
# def draw_lines(
#         img: Image.Image,
#         center: Tuple[int, int] = None,
# )
# def draw_lines(img):
#     img_copy = img.copy()
#     draw = ImageDraw.Draw(img_copy)

#     width, height = img_copy.size
#     center_x = width // 2
#     center_y = height // 2

#     # Vertical line
#     draw.line([(center_x, 0), (center_x, height)], fill=line_color, width=line_width)
#     # Horizontal line
#     draw.line([(0, center_y), (width, center_y)], fill=line_color, width=line_width)

#     return img_copy
