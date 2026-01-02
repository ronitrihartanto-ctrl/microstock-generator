import streamlit as st
import openai
import json
import pandas as pd
from PIL import Image
import numpy as np
from collections import Counter

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Microstock Metadata Generator", layout="wide")

if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY belum diset di Streamlit Secrets")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]

# ===============================
# COLOR DETECTION (LOCAL, STABLE)
# ===============================
COLOR_LABELS = {
    "blue": [0, 0, 255],
    "purple": [128, 0, 128],
    "green": [0, 128, 0],
    "red": [220, 20, 60],
    "orange": [255, 165, 0],
    "yellow": [255, 215, 0],
    "black": [0, 0, 0],
    "white": [255, 255, 255],
    "gray": [128, 128, 128],
    "pink": [255, 105, 180],
    "teal": [0, 128, 128],
    "cyan": [0, 255, 255],
}

def detect_main_color(img):
    img = img.resize((80, 80))
    pixels = np.array(img).reshape(-1, 3)

    def closest(rgb):
        r, g, b = rgb
        best, dist = "abstract", 1e9
        for name, ref in COLOR_LABELS.items():
            d = (r-ref[0])**2 + (g-ref[1])**2 + (b-ref[2])**2
            if d < dist:
                best, dist = name, d
        return best

    labels = [closest(p) for p in pixels]
    return Counter(labels).most_common(1)[0][0]

# ===============================
# AI METADATA (TEXT ONLY – SAFE)
# ===============================
def generate_metadata_ai(color):
    prompt = f"""
You are an Adobe Stock metadata expert.

Main color: {color}

Return ONLY valid JSON, no markdown, no explanation.

{{
  "title": "",
  "description": "",
  "keywords": []
}}

Rules:
- Keywords max 50
- SEO friendly
- No brand names
"""

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    text = response.choices[0].message.content.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "title": f"Abstract {color.capitalize()} Background",
            "description": f"Abstract {color} background suitable for web, presentation and digital design.",
            "keywords": [color, "abstract background", "design", "digital", "wallpaper"]
        }

# ===============================
# UI
# ===============================
st.title("🚀 Microstock Metadata Generator (STABLE)")
st.caption("No Vision • No eval • No crash • Streamlit-safe")

files = st.file_uploader(
    "Upload image(s)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

results = []

if files:
    for f in files:
        st.divider()
        img = Image.open(f).convert("RGB")
        st.image(img, width=300)

        color = detect_main_color(img)
        st.write("🎨 Detected color:", color)

        with st.spinner("Generating metadata..."):
            data = generate_metadata_ai(color)

        st.subheader("Title")
        st.write(data["title"])

        st.subheader("Description")
        st.write(data["description"])

        st.subheader("Keywords")
        st.write(", ".join(data["keywords"][:50]))

        results.append({
            "Filename": f.name,
            "Title": data["title"],
            "Description": data["description"],
            "Keywords": ", ".join(data["keywords"][:50])
        })

# ===============================
# CSV EXPORT
# ===============================
if results:
    st.divider()
    st.subheader("📦 Adobe Stock CSV")

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download CSV",
        csv,
        "adobe_stock_metadata.csv",
        "text/csv"
    )
