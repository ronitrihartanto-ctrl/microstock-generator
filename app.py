import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import colorsys
from collections import Counter
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Microstock Metadata Generator PRO",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Microstock Metadata Generator PRO")
st.caption("Adobe Stock Optimized • Auto Metadata • Export Ready")

# ---------------- COLOR DETECTION ----------------
def detect_main_color(image):
    img = image.resize((180, 180)).convert("RGB")
    pixels = np.array(img).reshape(-1, 3)

    bins = []

    for r, g, b in pixels:
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

        if v > 0.9 and s < 0.1:
            bins.append("white"); continue
        if v < 0.15:
            bins.append("black"); continue
        if s < 0.15:
            bins.append("gray"); continue

        if h < 0.04 or h > 0.96: bins.append("red")
        elif h < 0.08: bins.append("orange")
        elif h < 0.15: bins.append("yellow")
        elif h < 0.22: bins.append("lime")
        elif h < 0.35: bins.append("green")
        elif h < 0.45: bins.append("turquoise")
        elif h < 0.55: bins.append("cyan")
        elif h < 0.65: bins.append("blue")
        elif h < 0.72: bins.append("dark blue")
        elif h < 0.80: bins.append("purple")
        elif h < 0.88: bins.append("violet")
        else: bins.append("pink")

    counter = Counter(bins)
    if len(counter) > 6:
        return "colorful"

    dominant = counter.most_common(1)[0][0]
    if dominant in ["black", "white", "gray"]:
        return "monochrome"

    return dominant

# ---------------- SHAPE & STYLE ----------------
def detect_shapes_and_style(image):
    gray = image.convert("L").resize((200, 200))
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_density = np.mean(np.array(edges) > 40)

    blur = gray.filter(ImageFilter.GaussianBlur(radius=4))
    noise = np.mean(np.abs(np.array(gray) - np.array(blur)))

    shapes = []
    styles = []

    if edge_density < 0.02:
        shapes.append("smooth shapes")
        styles += ["minimal", "gradient"]
    elif edge_density < 0.05:
        shapes.append("waves")
        styles.append("fluid")
    elif edge_density < 0.10:
        shapes.append("lines")
        styles.append("modern")
    else:
        shapes += ["particles", "mesh"]
        styles.append("digital")

    styles.append("technology")
    styles.append("futuristic")

    if noise < 8:
        styles.append("clean")
    else:
        styles.append("dynamic")

    shapes.append("abstract shapes")

    return list(set(shapes)), list(set(styles))

# ---------------- TITLES ----------------
def generate_titles(color, shape, styles):
    base = [
        f"Abstract {color.capitalize()} {shape} Technology Background",
        f"Modern {color.capitalize()} Gradient {shape}",
        f"Futuristic {color.capitalize()} Abstract Digital Background",
        f"{color.capitalize()} {shape} Gradient Design for Technology",
        f"Abstract {color.capitalize()} Fluid Background"
    ]
    return base

# ---------------- ADOBE KEYWORDS ----------------
def generate_keywords(color, shapes, styles):
    keywords = [
        "abstract background",
        f"{color} background",
        "technology background",
        "gradient background",
        "abstract design",
        "modern background",
        "digital background",
        "futuristic design",
        "ui background",
        "website background",
        "app background",
        "presentation background",
        "corporate background",
        "business design",
        "branding",
        "marketing",
        "startup",
        "graphic design",
        "visual design",
        "abstract art"
    ]

    keywords += shapes
    keywords += styles

    clean = list(dict.fromkeys(keywords))
    return clean[:50]

# ---------------- UI ----------------
uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    st.image(image, use_column_width=True)

    color = detect_main_color(image)
    shapes, styles = detect_shapes_and_style(image)
    shape = shapes[0]

    titles = generate_titles(color, shape, styles)

    description = (
        f"Modern abstract background featuring {shape} with "
        f"{', '.join(styles[:2])} style in {color} color tones. "
        f"Perfect for technology projects, digital innovation, "
        f"websites, mobile applications, presentations, branding, "
        f"and Adobe Stock creative use."
    )

    keywords = generate_keywords(color, shapes, styles)

    st.subheader("📌 Titles (A/B Test)")
    for t in titles:
        st.write("•", t)

    st.subheader("📝 Description")
    st.write(description)

    st.subheader("🏷️ Keywords")
    st.code(", ".join(keywords))

    # EXPORT
    df = pd.DataFrame([{
        "Title": titles[0],
        "Description": description,
        "Keywords": ", ".join(keywords)
    }])

    st.download_button("⬇️ Download Adobe Stock CSV", df.to_csv(index=False), "adobe_stock.csv")
    st.download_button("⬇️ Download Titles TXT", "\n".join(titles), "titles.txt")
    st.download_button("⬇️ Download Description TXT", description, "description.txt")
    st.download_button("⬇️ Download Keywords TXT", ", ".join(keywords), "keywords.txt")

    st.success("PRO metadata generated & export ready ✔️")
