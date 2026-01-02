import streamlit as st
import openai
import json
import pandas as pd
import numpy as np
from PIL import Image

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Microstock Metadata Generator (STABLE)",
    layout="wide"
)

# ===============================
# OPENAI CONFIG
# ===============================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY belum diset di Streamlit Secrets")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]

# ===============================
# ADVANCED COLOR DETECTION
# ===============================
def detect_colors_advanced(img):
    img = img.resize((120, 120))
    pixels = np.array(img).reshape(-1, 3)

    colors = {
        "black": 0,
        "white": 0,
        "gray": 0,
        "gold": 0,
        "blue": 0,
        "red": 0,
        "green": 0,
        "purple": 0
    }

    for r, g, b in pixels:
        brightness = (r + g + b) / 3

        if brightness < 60:
            colors["black"] += 1
        elif brightness > 220:
            colors["white"] += 1
        elif r > 180 and g > 140 and b < 120:
            colors["gold"] += 1
        elif b > r and b > g:
            colors["blue"] += 1
        elif r > g and r > b:
            colors["red"] += 1
        elif g > r and g > b:
            colors["green"] += 1
        elif r > 120 and b > 120:
            colors["purple"] += 1
        else:
            colors["gray"] += 1

    sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_colors[0][0]
    secondary = sorted_colors[1][0]

    return primary, secondary

# ===============================
# AI METADATA GENERATOR (SAFE)
# ===============================
def generate_metadata_ai(color_text):
    prompt = f"""
You are an Adobe Stock metadata expert.

Main colors: {color_text}

Return ONLY valid JSON.
No markdown. No explanation.

Format:
{{
  "title": "",
  "description": "",
  "keywords": []
}}

Rules:
- Max 50 keywords
- SEO optimized
- Relevant to abstract background
- No brand names
"""

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=350
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except Exception:
        return {
            "title": f"Abstract {color_text.capitalize()} Background",
            "description": f"Modern abstract background with {color_text} colors, suitable for digital design, website, presentation, and marketing.",
            "keywords": color_text.split() + [
                "abstract background",
                "modern design",
                "digital background",
                "luxury",
                "technology"
            ]
        }

# ===============================
# UI
# ===============================
st.title("🚀 Microstock Metadata Generator (STABLE)")
st.caption("✔ Accurate color • ✔ No eval • ✔ No Vision • ✔ Adobe Stock ready")

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
        st.image(img, width=320)

        primary, secondary = detect_colors_advanced(img)
        color_text = f"{primary} and {secondary}"

        st.write(f"🎨 Detected colors: **{primary}**, **{secondary}**")

        with st.spinner("Generating metadata with AI..."):
            data = generate_metadata_ai(color_text)

        st.subheader("Title")
        st.write(data["title"])

        st.subheader("Description")
        st.write(data["description"])

        st.subheader("Keywords (50)")
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
    st.subheader("📦 Adobe Stock CSV Export")

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Adobe Stock CSV",
        csv,
        "adobe_stock_metadata.csv",
        "text/csv"
    )
