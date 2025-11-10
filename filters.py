import numpy as np
from enum import Enum
import cv2
from utils import preprocess_image


### ------ Filters
class Filters(Enum):
    BW = "Black & White"
    SEPIA = "sepia"


# Convert image to black and white - returns np array
def apply_black_and_white(img: np.ndarray) -> np.ndarray:
    img_copy = img.copy()
    img_preprocess = img_copy
    # img_preprocess = preprocess_image(img_copy, np.float32, normalize=True)

    if img_preprocess.shape[-1] == 4:
        img_rgb = img_preprocess[:, :, :3]
    else:
        img_rgb = img_preprocess

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    return img_gray


# Convert image to sepia - returns np array
def apply_sepia(img, intensity=1.0) -> np.ndarray:
    img_copy = img.copy()
    img_preprocess = img_copy
    # img_preprocess = preprocess_image(img_copy, np.float32, normalize=True)

    if img_preprocess.shape[-1] == 4:
        rgb = img_preprocess[..., :3]
    else:
        rgb = img_preprocess

    sepia_matrix = np.array(
        [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
    )

    sepia = rgb @ sepia_matrix.T
    sepia = np.clip(sepia, 0, 255)

    blended = rgb * (1 - intensity) + sepia * intensity
    img_preprocess[..., :3] = blended
    img_sepia = adjust_contrast(img_preprocess)

    return img_sepia


# Apply contrast on the image - returns np array
def adjust_contrast(img: np.ndarray, scale=0.0) -> np.ndarray:

    img_copy = img.copy()
    img_preprocess = img_copy
    # img_preprocess = preprocess_image(img_copy, np.float32, normalize=True)

    factor = 1.0 + scale
    midpoint = 127.5

    if img_preprocess.shape[-1] == 4:
        rgb = img_preprocess[..., :3]
        alpha = img_preprocess[..., 3:]
    else:
        rgb = img_preprocess
        alpha = None

    rgb = (rgb - midpoint) * factor + midpoint
    rgb = np.clip(rgb, 0, 255)

    if alpha is not None:
        img_contrast = np.concatenate([rgb, alpha], axis=-1)
    else:
        img_contrast = rgb

    # # Return in same dtype as input
    # if img.dtype == np.uint8:
    #     img_contrast = img_contrast.astype(np.uint8)

    return img_contrast


# Apply a filter based on the Filters enum -> returns 8 bit array
def apply_filter(
    img: np.ndarray, filter_type: Filters | None = None, intensity: float = 1.0
):
    # if filter_type is None:
    #     return preprocess_image(img, np.uint8)
    if filter_type is None:
        return img.copy()

    filters = {
        Filters.BW: apply_black_and_white,
        Filters.SEPIA: lambda x: apply_sepia(x, intensity=intensity),
    }

    if filter_type not in filters:
        raise ValueError(f"Unsupported filter: {filter_type}")

    img_filtered = filters[filter_type](img)
    return img_filtered
    # return preprocess_image(img_filtered, np.uint8)
