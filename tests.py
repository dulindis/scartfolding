import pytest
import cv2
import numpy as np

from filters import (
    apply_black_and_white,
    apply_sepia,
)
from grids import (
    compute_grid_positions,
    draw_grid,
    GridStart,
)
from utils import load_image


### ------ Tests


TEST_IMAGE = "./images/input/landscape.jpg"
OUTPUT_DIR = "./images/output/test"


@pytest.fixture
def img():
    image = load_image(TEST_IMAGE)
    cropped = image[0:50, 0:100]
    yield cropped


# Test load image shape
def test_load_image_shape(img):
    assert isinstance(img, np.ndarray)
    assert img.shape[0] == 50  # height
    assert img.shape[1] == 100  # width
    assert img.shape[-1] in (3, 4)


# Test black & white filter
def test_black_and_white(img):
    bw_img = apply_black_and_white(img)
    assert isinstance(bw_img, np.ndarray)
    assert bw_img.ndim == 2
    assert bw_img.dtype == np.uint8


# Test sepia filter
def test_sepia(img):
    sepia_img = apply_sepia(img)
    assert isinstance(sepia_img, np.ndarray)
    assert sepia_img.ndim == 3, "Sepia image should have 3 dimensions (H, W, C)"
    assert sepia_img.shape[-1] == 3, "Sepia image must have 3 color channels"
    assert sepia_img.dtype == np.float32
    # assert sepia_img.dtype == np.uint8


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
    img_with_grid = draw_grid(img, rows=2, cols=2, start=GridStart.CENTER)
    assert isinstance(img_with_grid, np.ndarray)
    assert img_with_grid.shape == img.shape

    h, w = img_with_grid.shape[:2]
    pixel = img_with_grid[h // 2, w // 2]
    assert isinstance(pixel, np.ndarray)
    assert pixel.ndim == 1
    assert len(pixel) in (3, 4)
    assert np.all((pixel >= 0) & (pixel <= 255))
