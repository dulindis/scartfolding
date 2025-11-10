import streamlit as st
from streamlit_image_comparison import image_comparison

from ratios import crop_to_ratio, Ratios
from grids import draw_grid, GridStart
from filters import apply_filter, Filters
from utils import load_image, image_to_bytes, preprocess_image, to_uint8_rgb
import numpy as np
from posterify import posterify

st.title("🖼️ Image Prep App - scARTfolding")

# Initialize session state
if "last_ratio" not in st.session_state:
    st.session_state.last_ratio = "None"

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded:
    img = load_image(uploaded)

    # Ratio crop options
    st.subheader("✂️ Ratio Crop Options")

    ratio_choices = [None] + list(Ratios)
    ratio_option = st.selectbox(
        "Choose a ratio variant",
        ratio_choices,
        index=0,
        format_func=lambda r: "None" if r is None else r.name,
    )
    selected_ratio = ratio_option

    ratio_changed = selected_ratio != st.session_state.last_ratio
    st.session_state.last_ratio = selected_ratio

    cropped_img = crop_to_ratio(img, selected_ratio)

    # for further processing
    img_working = preprocess_image(
        cropped_img, target_dtype=np.float32, normalize=False
    )

    # Filter selection
    st.subheader("🎨 Filters")

    filter_choices = [None] + list(Filters)
    filter_option = st.selectbox(
        "Choose a filter",
        filter_choices,
        index=0,
        format_func=lambda f: "None" if f is None else f.value,
    )

    selected_filter = filter_option

    intensity = 0.8
    if selected_filter == Filters.SEPIA:
        intensity = st.slider("Sepia intensity", 0.0, 1.0, 0.8, 0.1)

    filtered_img = apply_filter(img_working, selected_filter, intensity=intensity)
    #     filtered_img = apply_filter(
    #     crop_to_ratio(img_working, selected_ratio), selected_filter, intensity=intensity
    # )

    # Posterify options
    st.subheader("🖼️ Posterify Options")

    k = st.slider("Number of color levels (k)", 2, 20, 5, 1)

    apply_posterify = st.checkbox("Apply Posterify")

    if apply_posterify:
        from posterify import posterify

        processed_img = posterify(filtered_img, k=k)
    else:
        processed_img = filtered_img
    # processed_img = posterify(filtered_img, k=k)
    # if st.button("Apply Posterify"):
    #     from posterify import posterify

    #     processed_img = posterify(filtered_img, k=k)
    # else:
    #     processed_img = filtered_img

    # st.subheader("Posterifyed Image")

    # st.image(
    #     to_uint8_rgb(processed_img),
    #     width=800,
    # )

    # Grid options
    st.subheader("📐 Grid Overlay")

    start_mode = st.selectbox("Grid start", [e.value for e in GridStart])
    start_enum = next(e for e in GridStart if e.value == start_mode)

    rows = st.slider("Rows", 1, 10, 3)
    cols = st.slider("Cols", 1, 10, 3)

    # TODO: create a pipeline for modifications
    # Apply grid
    # processed_img = draw_grid(filtered_img, start=start_enum, rows=rows, cols=cols)
    # processed_img = draw_grid(filtered_img, start=start_enum, rows=rows, cols=cols)
    processed_img = draw_grid(processed_img, start=start_enum, rows=rows, cols=cols)

    st.subheader("🔍 Before vs After")

    preview_cropped = to_uint8_rgb(cropped_img)  # always shows the initial ratio crop
    processed_preview = to_uint8_rgb(processed_img)  # final processed image

    # preview_cropped = preprocess_image(cropped_img, target_dtype=np.uint8)

    # image_comparison(
    #     img1=cropped_img,
    #     img2=processed_img,
    #     label1=f"Original",
    #     label2=f"Processed",
    #     width=800,
    # )

    image_comparison(
        img1=preview_cropped,
        img2=processed_preview,
        label1="Original",
        label2="Processed",
        width=800,
    )
    # st.image(processed_preview, width=800)

    byte_data = image_to_bytes(processed_img, format="PNG")

    st.subheader("📥 Download processed image")

    st.download_button(
        label=f"Download - PNG",
        data=byte_data,
        file_name="processed_image.png",
        mime="image/png",
    )
    st.download_button(
        label=f"Download - JPG",
        data=byte_data,
        file_name="processed_image.jpg",
        mime="image/jpg",
    )
