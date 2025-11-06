from PIL import Image
import numpy as np
from enum import Enum

from utils import load_image

# , image_to_bytes


### ------ Filters
class Filters(Enum):
    BW = "black_and_white"
    SEPIA = "sepia"


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


# Apply a filter based on the Filters enum
def apply_filter(img, filter_type: Filters | None = None, intensity: float = 1.0):
    if filter_type is None:
        return img.copy()
    if filter_type == Filters.BW:
        return apply_black_and_white(img)
    elif filter_type == Filters.SEPIA:
        return apply_sepia(img, intensity=intensity)
    else:
        raise ValueError(f"Unsupported filter: {filter_type}")
