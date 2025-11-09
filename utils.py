import cv2
import numpy as np

### ------ Utility Functions


# Load Image - takes either a file path or file-like object and returns a NumPy array representing the image.
def load_image(file, keep_alpha=False) -> np.ndarray:

    if hasattr(file, "read"):
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
    else:
        img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ValueError("Could not load image")

    if keep_alpha:
        if img.shape[-1] == 3:
            alpha = np.full((img.shape[0], img.shape[1], 1), 255, dtype=np.uint8)
            img = np.concatenate([img, alpha], axis=-1)
        elif img.shape[-1] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    else:
        if img.shape[-1] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

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


def to_uint8(img: np.ndarray) -> np.ndarray:
    return np.clip(img, 0, 255).astype(np.uint8)
