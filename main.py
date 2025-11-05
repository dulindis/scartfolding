import streamlit as st
from streamlit_image_comparison import image_comparison

from grids import draw_grid, GridStart
from filters import apply_filter, Filters, load_image
from utils import load_image, image_to_bytes


st.title("🖼️ Image Prep App - scARTfolding")

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded:
    img = load_image(uploaded)

    # Filter selection
    st.subheader("🎨 Filters")

    filter_option = st.selectbox(
        "Choose a filter",
        [f.value for f in Filters],
        index=0,
    )

    selected_filter = next(f for f in Filters if f.value == filter_option)

    intensity = 0.8
    if selected_filter == Filters.SEPIA:
        intensity = st.slider("Sepia intensity", 0.0, 1.0, 0.8, 0.1)

    filtered_img = apply_filter(img, selected_filter, intensity=intensity)

    # Grid options
    st.subheader("📐 Grid Overlay")

    start_mode = st.selectbox("Grid start", [e.value for e in GridStart])
    start_enum = next(e for e in GridStart if e.value == start_mode)

    rows = st.slider("Rows", 1, 10, 3)
    cols = st.slider("Cols", 1, 10, 3)

    # Apply grid
    img_with_grid = draw_grid(filtered_img, start=start_enum, rows=rows, cols=cols)

    st.subheader("🔍 Before vs After")
    image_comparison(
        img1=img,
        img2=img_with_grid,
        label1="Original",
        label2="Processed",
        width=800,
    )
    # Show preview - single view
    # st.image(img_with_grid, caption="Preview", use_column_width=True)

    byte_data = image_to_bytes(img_with_grid, format="PNG")

    st.download_button(
        label="📥 Download processed image",
        data=byte_data,
        file_name="processed_image.png",
        mime="image/png",
    )
