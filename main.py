import streamlit as st
from streamlit_image_comparison import image_comparison

from ratios import crop_to_ratio, Ratios
from grids import draw_grid, GridStart
from filters import apply_filter, Filters, load_image
from utils import load_image, image_to_bytes


st.title("🖼️ Image Prep App - scARTfolding")

# Initialize session state
if "last_ratio" not in st.session_state:
    st.session_state.last_ratio = "None"

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded:
    img = load_image(uploaded)

    # Ratio crop options
    st.subheader("✂️ Ratio Crop Options")

    ratio_choices = ["None"] + [r.name for r in Ratios]
    ratio_option = st.selectbox(
        "Choose a ratio variant",
        ratio_choices,
        index=0,
    )
    selected_ratio = None if ratio_option == "None" else Ratios[ratio_option]

    ratio_changed = selected_ratio != st.session_state.last_ratio
    st.session_state.last_ratio = selected_ratio

    # selected_ratio = next((r for r in Ratios if r.value == ratio_option), None)

    cropped_img = crop_to_ratio(img, selected_ratio)

    # Filter selection
    st.subheader("🎨 Filters")

    filter_choices = ["None"] + [f.value for f in Filters]
    filter_option = st.selectbox(
        "Choose a filter",
        filter_choices,
        index=0,
    )

    # selected_filter = next((f for f in Filters if f.value == filter_option), None)
    selected_filter = (
        None
        if filter_option == "None"
        else next(f for f in Filters if f.value == filter_option)
    )

    intensity = 0.8
    if selected_filter == Filters.SEPIA:
        intensity = st.slider("Sepia intensity", 0.0, 1.0, 0.8, 0.1)

    filtered_img = apply_filter(cropped_img, selected_filter, intensity=intensity)

    # Grid options
    st.subheader("📐 Grid Overlay")

    start_mode = st.selectbox("Grid start", [e.value for e in GridStart])
    start_enum = next(e for e in GridStart if e.value == start_mode)

    rows = st.slider("Rows", 1, 10, 3)
    cols = st.slider("Cols", 1, 10, 3)

    # Apply grid
    processed_img = draw_grid(filtered_img, start=start_enum, rows=rows, cols=cols)

    st.subheader("🔍 Before vs After")
    image_comparison(
        img1=cropped_img,
        img2=processed_img,
        label1=f"Original",
        label2=f"Processed",
        width=800,
    )

    byte_data = image_to_bytes(processed_img, format="PNG")

    st.subheader("💾 Download processed image")

    st.download_button(
        label=f"📥 Download - PNG",
        data=byte_data,
        file_name="processed_image.png",
        mime="image/png",
    )
    st.download_button(
        label=f"📥 Download - JPG",
        data=byte_data,
        file_name="processed_image.jpg",
        mime="image/jpg",
    )
