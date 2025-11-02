import pytest
from pathlib import Path
from PIL import Image
from filters import (
    load_image,
    apply_black_and_white,
    apply_sepia,
    save_image,
)
from grids import (
    find_center,
    compute_axis,
    determine_starting_point,
    compute_positions,
    draw_grid,
)


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


# Test saving filtered image
def test_save_image(img, tmp_path):
    tmp_file = tmp_path / "test_bw.jpg"
    img.save(tmp_file)
    assert tmp_file.exists()


# Test find_center
def test_find_center(img):
    cx, cy = find_center(img)
    assert cx == 50
    assert cy == 25


def test_compute_axis_default(img):
    cx, cy = compute_axis(img)
    assert (cx, cy) == (50, 25)


def test_compute_axis_with_values(img):
    cx, cy = compute_axis(img, central_x=10, central_y=20)
    assert (cx, cy) == (10, 20)


# Test determine_starting_point
def test_determine_starting_point_center():
    x, y = determine_starting_point("center", 100, 50)
    assert (x, y) == (50, 25)


def test_determine_starting_point_left():
    x, y = determine_starting_point("left", 100, 50)
    assert (x, y) == (0, 0)


def test_determine_starting_point_right():
    x, y = determine_starting_point("right", 100, 50)
    assert (x, y) == (100, 0)


def test_determine_starting_point_invalid():
    import pytest

    with pytest.raises(ValueError):
        determine_starting_point("top", 100, 50)


# Test compute_positions
def test_compute_positions_default():
    seg, pos = compute_positions(100)
    assert seg == 100
    assert pos == [0]


def test_compute_positions_count():
    seg, pos = compute_positions(100, count=4)
    assert seg == 25
    assert pos == [0, 25, 50, 75]


def test_compute_positions_spacing():
    seg, pos = compute_positions(100, spacing=20)
    assert seg == 20
    assert pos == [0, 20, 40, 60, 80]


def test_compute_positions_count_spacing():
    seg, pos = compute_positions(100, count=3, spacing=30)
    assert seg == 30
    assert pos == [0, 30, 60]


# Test draw_grid
def test_draw_grid_basic(img):
    img_with_grid = draw_grid(img, rows=2, cols=2)
    assert isinstance(img_with_grid, Image.Image)
    # Ensure original image not modified
    assert img != img_with_grid
    # Optional: check a pixel that should be colored
    # (not too strict, just basic sanity)
    width, height = img_with_grid.size
    pixel = img_with_grid.getpixel((width // 2, height // 2))
    assert isinstance(pixel, tuple) and len(pixel) == 3
