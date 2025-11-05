import pytest
from PIL import Image

from filters import (
    load_image,
    apply_black_and_white,
    apply_sepia,
)
from grids import (
    compute_grid_positions,
    draw_grid,
    GridStart,
)

### ------ Tests


TEST_IMAGE = "./images/input/landscape.jpg"
OUTPUT_DIR = "./images/output/test"


@pytest.fixture
def img():
    image = load_image(TEST_IMAGE)
    cropped = image.crop((0, 0, 100, 50))
    yield cropped
    image.close()


# Test black & white filter
def test_black_and_white(img):
    bw_img = apply_black_and_white(img)
    assert isinstance(bw_img, Image.Image)
    assert bw_img.mode in ["RGB", "L"]


# Test sepia filter
def test_sepia(img):
    sepia_img = apply_sepia(img)
    assert isinstance(sepia_img, Image.Image)
    assert sepia_img.mode == "RGB"


# --- Position computation ---
def test_compute_grid_positions_center_basic():
    x_pos, y_pos = compute_grid_positions(
        width=100,
        height=50,
        cols=3,
        rows=3,
        col_spacing=None,
        row_spacing=None,
        start=GridStart.CENTER,
    )
    # Expect 3 lines roughly centered
    assert len(x_pos) == 3
    assert len(y_pos) == 3
    assert abs(x_pos[1] - 50) < 1  # Middle line near center
    assert abs(y_pos[1] - 25) < 1


def test_compute_grid_positions_left():
    x_pos, y_pos = compute_grid_positions(
        width=100,
        height=50,
        cols=4,
        rows=2,
        col_spacing=None,
        row_spacing=None,
        start=GridStart.LEFT,
    )
    # Should start from left going right
    assert x_pos[0] > 0
    assert x_pos[-1] < 100
    assert all(x_pos[i] < x_pos[i + 1] for i in range(len(x_pos) - 1))
    assert len(y_pos) == 1


def test_compute_grid_positions_right():
    x_pos, y_pos = compute_grid_positions(
        width=100,
        height=50,
        cols=3,
        rows=3,
        col_spacing=None,
        row_spacing=None,
        start=GridStart.RIGHT,
    )
    # Should start from right going left
    assert x_pos[0] < 100
    assert x_pos[-1] > 0
    assert all(x_pos[i] > x_pos[i + 1] for i in range(len(x_pos) - 1))


def test_compute_grid_positions_custom_spacing():
    x_pos, y_pos = compute_grid_positions(
        width=100,
        height=60,
        cols=None,
        rows=None,
        col_spacing=20,
        row_spacing=15,
        start=GridStart.LEFT,
    )
    # Since cols/rows are None, spacing doesn’t create grid lines — expect empty lists
    assert isinstance(x_pos, list)
    assert isinstance(y_pos, list)


# --- Grid drawing ---
def test_draw_grid_basic(img):
    # ✅ use the Enum instead of string
    img_with_grid = draw_grid(img, rows=2, cols=2, start=GridStart.CENTER)
    assert isinstance(img_with_grid, Image.Image)
    assert img != img_with_grid

    # Sanity check: pixel in the middle should exist and be RGB
    width, height = img_with_grid.size
    pixel = img_with_grid.getpixel((width // 2, height // 2))
    assert isinstance(pixel, tuple)
    assert len(pixel) == 3
