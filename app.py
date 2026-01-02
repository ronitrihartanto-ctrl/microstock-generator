import streamlit as st
from PIL import Image
import numpy as np
import colorsys

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Microstock Metadata Generator",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 Microstock Metadata Generator")
st.caption("Upload image → Auto Title, Description & 50 Keywords")

# ---------------- COLOR DETECTION ----------------
def detect_main_color(image):
    img = image.resize((150, 150)).convert("RGB")
    pixels = np.array(img).reshape(-1, 3)

    hues = []

    for r, g, b in pixels:
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

        # Abaikan warna terlalu gelap (background)
        if v < 0.25:
            continue

        # Fokus ke warna cukup kuat
        if s > 0.35:
            hues.append(h)

    if not hues:
        return "dark"

    avg_hue = sum(hues) / len(hues)

    if 0.55 <= avg_hue <= 0.72:
        return "blue"
    elif 0.72 < avg_hue <= 0.85:
        return "purple"
    elif 0.25 <= avg_hue < 0.45:
        return "green"
    elif avg_hue < 0.05 or avg_hue > 0.95:
        return "red"
    else:
        return "colorful"

# ---------------- STYLE DETECTION ----------------
def detect_style(image):
    w, h = image.size
    if w > h:
        return "technology background"
    elif w == h:
        return "abstract background"
    else:
        return "abstract design"

# ---------------- KEYWORDS ----------------
def generate_keywords(color):
    base_keywords = [
        "abstract", "background", "abstract background", "technology",
        f"{color} background", "gradient", "modern", "digital", "wave",
        "circles", "abstract design", "technology background", "geometric",
        "shapes", "fluid", "flow", "smooth", "futuristic", "creative",
        "minimal", "clean", "corporate", "business", "innovation",
        "ui", "ux", "interface", "website background", "app background",
        "presentation", "banner", "poster", "wallpaper", "digital background",
        "modern background", "tech", "startup", "social media", "marketing",
        "design template", "dynamic", "contemporary", "gradient background",
        "technology design"
    ]
    return base_keywords[:50]

# ---------------- UI ----------------
uploaded_file = st.file_uploader(
    "Upload Image (JPG / PNG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)

    color = detect_main_color(image)
    style = detect_style(image)

    title = f"Abstract {color.capitalize()} {style} with Gradient Shapes"

    description = (
        f"Modern abstract {style} featuring smooth gradient shapes "
        f"in {color} tones. Clean and dynamic design suitable for "
        f"technology concepts, digital innovation, websites, mobile "
        f"applications, presentations, banners, UI design, and "
        f"corporate branding."
    )

    keywords = generate_keywords(color)

    st.subheader("📌 Title")
    st.code(title)

    st.subheader("📝 Description")
    st.write(description)

    st.subheader("🏷️ 50 Keywords")
    st.code(", ".join(keywords))

    st.success("Metadata generated successfully ✔️")
