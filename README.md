# 🎨 scARTfolding — Image Preparation App

**Live Demo:** [scARTfolding on Streamlit ↗](https://scartfolding-ygwnhxqbndqhrdfgzll6tb.streamlit.app/)

---

## 🖼️ Overview

**scARTfolding** is a modern, browser-based tool that helps you prepare and stylize images for creative or analytical purposes.  
It allows you to **upload an image**, **apply filters**, and **overlay grids** — all with instant preview to help your artistic process.

Ideal for:

- Artists preparing drawing references
- Designers testing layout balance
- Creators exploring symmetry and structure

---

## ⚡ Features

✅ Upload images (`.jpg`, `.jpeg`, `.png`)

✅ Crop to built-in aspect ratios

✅ Apply built-in filters

- 🖤 Black & White
- 🟤 Sepia

✅ Add adjustable grids

- Set number of rows & columns
- Control starting alignment (Left / Center / Right)
- Frame edges automatically

✅ Compare results interactively

- View before & after images side by side

✅ Download processed images instantly

---

## 🚀 Try It Online

👉 **[Open scARTfolding App](https://scartfolding-ygwnhxqbndqhrdfgzll6tb.streamlit.app/)**

No installation required.

---

## 🧩 Tech Stack

- **Python 3.13+**
- **Streamlit** — app framework
- **Pillow (PIL)** — image processing
- **NumPy** — array manipulation
- **streamlit-image-comparison** — visual comparison slider

---

## 💻 Local Setup

To run locally:

```bash
# 1️⃣ Clone the repository
git clone https://github.com/<your-username>/scartfolding.git
cd scartfolding

# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run the app
streamlit run main.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📂 Project Structure

```
scartfolding/
├── main.py                   # Streamlit app entry point
├── grids.py                  # Grid rendering utilities
├── filters.py                # Image filter logic (with Enum)
├── utils.py                  # Helper functions (load/save)
├── tests/                    # Unit tests (pytest)
├── requirements.txt
└── README.md
```

---

## 🧱 Future Enhancements

- [ ] Add brightness/contrast controls
- [ ] Fine-tune ratio cropping UI
- [ ] Support SVG export for grid overlays
- [ ] New artistic filters (warm, cool, sketch, duotone)
- [ ] Touch-friendly mobile interface
- [ ] Variantify - AI powered variants to give you creative spark and unleash tweaking.
- [ ] Posterify - AI powered variants to give you creative spark and unleash tweaking.

---

## 🖋️ Author

Created by [**Paulina (@dulindis)**](https://github.com/dulindis)  
Built with ❤️ for art, geometry, and creative exploration.

---

## ⚖️ Usage Terms

© 2025 Paulina. All rights reserved.

This software and its visual output are **not licensed for AI training, dataset creation, or machine learning use** in any form, in compliance with the **EU AI Act** and related data ethics standards.

You may use this app for **personal and artistic purposes only**.  
Reproduction, redistribution, or automated data collection from this tool is **strictly prohibited** without explicit written permission.
