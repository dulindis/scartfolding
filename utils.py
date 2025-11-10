import cv2
import numpy as np
import traceback


### ------ Utility Functions


# Load Image - takes either a file path or file-like object and returns a NumPy array representing the image float 8.
def load_image(file, keep_alpha=True, as_float32=False) -> np.ndarray:

    if hasattr(file, "read"):
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
    else:
        img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ValueError("Could not load image")

    # 2️⃣ Handle channels
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        if keep_alpha:
            alpha = np.full((img.shape[0], img.shape[1], 1), 255, dtype=np.uint8)
            img = np.concatenate([img, alpha], axis=-1)
    elif img.shape[-1] == 3:
        if keep_alpha:
            alpha = np.full((img.shape[0], img.shape[1], 1), 255, dtype=np.uint8)
            img = np.concatenate([img, alpha], axis=-1)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif img.shape[-1] == 4:
        if keep_alpha:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

    # 3️⃣ Preprocess dtype / normalization
    img = preprocess_image(
        img, target_dtype=np.float32 if as_float32 else np.uint8, normalize=as_float32
    )

    return img


def image_to_bytes(img_array: np.ndarray, format="PNG") -> bytes:

    if img_array is None:
        raise ValueError("Input image array is None")

    if img_array.dtype != np.uint8:
        img = img.astype(np.uint8)

    if img_array.ndim == 3:
        if img_array.shape[-1] == 3:  # RGB
            img_enc = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        elif img_array.shape[-1] == 4:  # RGBA
            img_enc = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGRA)
        else:
            raise ValueError(f"Unsupported channel count: {img_array.shape[-1]}")
    elif img_array.ndim == 2:
        img_enc = img_array
    else:
        raise ValueError("Unsupported image shape — expected (H, W) or (H, W, C)")

    ext = f".{format.lower()}"
    success, encoded_img = cv2.imencode(ext, img_enc)
    if not success:
        raise ValueError(f"Could not encode image to {format.upper()}")

    return encoded_img.tobytes()


def preprocess_image(
    img: np.ndarray,
    target_dtype=np.uint8,
    normalize: bool = False,
    check_range: bool = True,
) -> np.ndarray:
    """
    Fully reusable image preprocessing function.

    Parameters:
        img (np.ndarray): Input image.
        target_dtype (np.dtype): Desired dtype, np.uint8 or np.float32.
        normalize (bool): If True and target_dtype=float32, scale to [0,1].
        check_range (bool): Validate that values are within expected range.

    Returns:
        np.ndarray: Preprocessed image.
    """
    # 1️⃣ Validate input
    if not isinstance(img, np.ndarray):
        raise TypeError("img must be a numpy.ndarray")
    if img.size == 0:
        raise ValueError("img is empty")

    # 2️⃣ Optional range check
    if check_range:
        if img.dtype == np.uint8:
            if img.min() < 0 or img.max() > 255:
                raise ValueError("uint8 image has values outside [0, 255]")
        elif img.dtype == np.float32:
            if img.min() < 0.0 or img.max() > 1.0:
                print("Warning: float32 image has values outside [0.0, 1.0]")
                traceback.print_stack(limit=3)

    # 3️⃣ Convert dtype if needed
    if target_dtype == np.float32:
        img = img.astype(np.float32)
        if normalize:
            # Automatically normalize if original was uint8
            if img.max() > 1.0:
                img /= 255.0
    elif target_dtype == np.uint8:
        # Clip values to valid range for uint8
        img = np.clip(img, 0, 255).astype(np.uint8)
    else:
        raise TypeError("target_dtype must be np.uint8 or np.float32")

    return img
