from enum import Enum
import numpy as np


# Various ratio cropping
class Ratios(Enum):
    SQUARE = (1, 1)
    STANDARD_PHOTO_VERTICAL = (2, 3)
    STANDARD_PHOTO_HORIZONTAL = (3, 2)
    WIDESCREEN = (16, 9)
    CINEMATIC = (21, 9)
    CLASSIC_TV = (4, 3)
    PORTRAIT = (4, 5)
    MEDIUM_FORMAT = (3, 2)
    STORY_VERTICAL = (9, 16)
    STORY_HORIZONTAL = (9, 16)


def crop_to_ratio(
    img: np.ndarray, ratio: Ratios | None = None, center: bool = True
) -> np.ndarray:

    height, width = img.shape[:2]
    current_ratio = width / height

    if ratio is None:
        return img.copy()

    w_ratio, h_ratio = ratio.value
    target_ratio = w_ratio / h_ratio

    EPSILON = 1e-6
    if abs(current_ratio - target_ratio) < EPSILON:
        return img.copy()

    if current_ratio > target_ratio:
        new_height = height
        new_width = int(round(height * target_ratio))
    elif current_ratio < target_ratio:
        new_width = width
        # new_height = int(round(width * target_ratio))
        new_height = int(round(width / target_ratio))

    else:
        return img.copy()

    if center:
        left = int(round((width - new_width) / 2))
        top = int(round((height - new_height) / 2))
    else:
        left, top = 0, 0

    right = left + new_width
    bottom = top + new_height

    cropped_img = img[top:bottom, left:right].copy()
    return cropped_img
