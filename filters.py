import numpy as np
from enum import Enum
import cv2

from utils import to_uint8


### ------ Filters
class Filters(Enum):
    BW = "Black & White"
    SEPIA = "sepia"


# Convert image to black and white - returns np array
def apply_black_and_white(img: np.ndarray) -> np.ndarray:
    if img.shape[-1] == 4:
        img_rgb = img[:, :, :3]
    else:
        img_rgb = img
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    return img_gray


# Convert image to sepia - returns np array
def apply_sepia(img, intensity=1.0) -> np.ndarray:
    img_copy = img.astype(np.float32)

    sepia_matrix = np.array(
        [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
    )

    rgb = img_copy[..., :3]
    sepia = rgb @ sepia_matrix.T
    sepia = np.clip(sepia, 0, 255)

    img_copy[..., :3] = rgb * (1 - intensity) + sepia * intensity
    img_copy = adjust_contrast(img_copy)
    return img_copy


# Apply contrast on the image - returns np array
def adjust_contrast(img: np.ndarray, scale=0.0) -> np.ndarray:

    img_copy = img.astype(np.float32)

    factor = 1.0 + scale
    midpoint = 127.5

    img_copy[..., :3] = (img_copy[..., :3] - midpoint) * factor + midpoint
    img_copy[..., :3] = np.clip(img_copy[..., :3], 0, 255)

    return img_copy


# Apply a filter based on the Filters enum -> returns 8 bit array
def apply_filter(
    img: np.ndarray, filter_type: Filters | None = None, intensity: float = 1.0
):
    if filter_type is None:
        return to_uint8(img)  # TODO: rething uint8 placement

    filters = {
        Filters.BW: apply_black_and_white,
        Filters.SEPIA: lambda x: apply_sepia(x, intensity=intensity),
    }

    if filter_type not in filters:
        raise ValueError(f"Unsupported filter: {filter_type}")

    img_filtered = filters[filter_type](img)
    return to_uint8(img_filtered)
