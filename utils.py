from io import BytesIO
from PIL import Image
from pathlib import Path

### ------ Utility Functions


# Load Image - returns PIL img
def load_image(source):
    if isinstance(source, (str, Path)):
        return Image.open(source)
    elif hasattr(source, "read"):  # file-like (like from st.file_uploader)
        return Image.open(source)
    else:
        raise TypeError("Unsupported source type for load_image")


def image_to_bytes(img, format="PNG"):

    buf = BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()
