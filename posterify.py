from enum import Enum
import numpy as np
from utils import load_image, preprocess_image
import cv2
from typing import Tuple, Optional


# def detect_edges(img):
#     np_img = np.array(img, dtype=np.float32)
#     return


# maybe better to take a pic and convert on the go to be more memory efficient ?
# Takes a nupmy array of np.float32 data type and nclusters(k) Number of clusters required at end
def posterify(
    img: np.ndarray,
    k: int = 5,
    criteria: Optional[Tuple[int, int, float]] = None,
    attempts: int = 5,
    flags: int = cv2.KMEANS_PP_CENTERS,
    convert_to_lab: bool = False,
    preserve_alpha: bool = True,
) -> np.ndarray:
    """
    Posterize an image by clustering pixel colors using cv2.kmeans.

    Parameters
    ----------
    img : np.ndarray
        Input image. dtype should be uint8, shape (H, W) for grayscale or (H, W, C) for color.
    k : int
        Number of color clusters (levels).
    criteria : tuple or None
        Termination criteria for kmeans: (type, max_iter, epsilon).
        If None, defaults to (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0).
    attempts : int
        Number of times the kmeans algorithm is executed using different initial labellings.
    flags : int
        Initialization flag: cv2.KMEANS_PP_CENTERS or cv2.KMEANS_RANDOM_CENTERS.
    convert_to_lab : bool
        If True, convert BGR->LAB before clustering and back after. Helps perceptual grouping.
    preserve_alpha : bool
        If True and image has 4 channels, preserve alpha channel unchanged.

    Returns
    -------
    np.ndarray
        Posterized image, same shape and dtype as input (uint8).
    """
    img = preprocess_image(img, np.float32)

    if img.size == 0:
        return img.copy()

    # Handle alpha channel
    alpha = None
    if img.ndim == 3 and img.shape[2] == 4:
        if preserve_alpha:
            alpha = img[:, :, 3].copy()
            img = img[:, :, :3]
        else:
            # ignore alpha channel in clustering but keep it later
            img = img[:, :, :3]
    # Optionally convert color space (BGR -> LAB) to get perceptually better clusters
    img_proc = img
    if convert_to_lab:
        img_proc = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    h, w = img_proc.shape[:2]
    channels = 1 if img_proc.ndim == 2 else img_proc.shape[2]

    # Reshape to (N, C)
    samples = img_proc.reshape((-1, channels)).astype(np.float32)

    # Default criteria
    if criteria is None:
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Run kmeans
    compactness, labels, centers = cv2.kmeans(
        samples, k, None, criteria, attempts, flags
    )

    # centers: (k, C) float32 -> convert to uint8
    centers_uint8 = centers.astype(np.uint8)

    # Map each label to the center color
    result_flat = centers_uint8[labels.flatten()]
    result = (
        result_flat.reshape((h, w, channels))
        if channels > 1
        else result_flat.reshape((h, w))
    )

    # Convert back color space if needed
    if convert_to_lab:
        result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)

    # Reattach alpha if present
    if alpha is not None:
        # ensure alpha shape (h, w)
        if result.ndim == 2:
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        result = np.dstack([result, alpha])

    return result.astype(np.uint8)
