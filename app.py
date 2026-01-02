import streamlit as st
import openai
import pandas as pd
from PIL import Image
import numpy as np
from collections import Counter

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Microstock Metadata Generator", layout="wide")

if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY belum diset")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]

# ===============================
# COLOR DETECTION (LOCAL & AKURAT)
# ===============================
COLOR_MAP = {
    "blue": [(0, 0, 255), (70, 130, 180)],
    "purple": [(128, 0, 128)],
    "green": [(0, 128, 0)],
    "red": [(220, 20, 60)],
    "orange": [(255, 165, 0)],
    "yellow": [(255, 215, 0)],
    "black": [(0, 0, 0)],
    "white": [(255, 255, 255)],
    "gray": [(128, 128, 128)],
    "pink": [(255, 105, 180)],
    "teal": [(0, 128, 128)],
    "cyan": [(0, 255, 255)],
}

def closest_color(rgb):
    r, g, b = rgb
    min_dist = 1e9
    name = "abstract"
    for color, samples in COLOR_MAP.items():
        for s in samples:
            dist = (r-s[0])**2 + (g-s[1])**2 + (b-s[2])**2
            if dist < min_dist:
                min_dist = dist
                name = color
    return name

def detect_main_color(img):
    img = img.resize((100, 100))
    pixels = np.array(img).reshape(-1, 3)
    colors = [closest_color(tuple(p)) for p in pixels]
    return Counter(colors).most_common(1)[0][0]

# ===============================
# AI TEXT GENERATOR (STABLE)
# ===============================
def generate_metadata_ai(color):
    prompt = f"""
Create Adobe Stock metadata.

Main color: {color}

Return JSON only:
{{
 "title": "",
 "description": "",
 "keywords": []
}}

Rules:
- Keywords max 50
- No brand names
- SEO friendly
"""

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return eval(response.choices[0].message.content)

# ===============================
# UI
# ===============================
st.title("🚀 Microstock Metadata Generator (STABLE)")
st.caption("Color detection lokal + AI metadata (NO vision error)")

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
        st.write(", ".join(data["keywords"]))

        results.append({
            "Filename": f.name,
            "Title": data["title"],
            "Description": data["description"],
            "Keywords": ", ".join(data["keywords"])
        })

# ===============================
# CSV EXPORT
# ===============================
if results:
    df = pd.DataFrame(results)
    st.divider()
    st.subheader("📦 Adobe Stock CSV")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download CSV",
        csv,
        "adobe_stock_metadata.csv",
        "text/csv"
    )
import streamlit as st
import openai
import pandas as pd
from PIL import Image
import numpy as np
from collections import Counter

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Microstock Metadata Generator", layout="wide")

if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY belum diset")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]

# ===============================
# COLOR DETECTION (LOCAL & AKURAT)
# ===============================
COLOR_MAP = {
    "blue": [(0, 0, 255), (70, 130, 180)],
    "purple": [(128, 0, 128)],
    "green": [(0, 128, 0)],
    "red": [(220, 20, 60)],
    "orange": [(255, 165, 0)],
    "yellow": [(255, 215, 0)],
    "black": [(0, 0, 0)],
    "white": [(255, 255, 255)],
    "gray": [(128, 128, 128)],
    "pink": [(255, 105, 180)],
    "teal": [(0, 128, 128)],
    "cyan": [(0, 255, 255)],
}

def closest_color(rgb):
    r, g, b = rgb
    min_dist = 1e9
    name = "abstract"
    for color, samples in COLOR_MAP.items():
        for s in samples:
            dist = (r-s[0])**2 + (g-s[1])**2 + (b-s[2])**2
            if dist < min_dist:
                min_dist = dist
                name = color
    return name

def detect_main_color(img):
    img = img.resize((100, 100))
    pixels = np.array(img).reshape(-1, 3)
    colors = [closest_color(tuple(p)) for p in pixels]
    return Counter(colors).most_common(1)[0][0]

# ===============================
# AI TEXT GENERATOR (STABLE)
# ===============================
def generate_metadata_ai(color):
    prompt = f"""
Create Adobe Stock metadata.

Main color: {color}

Return JSON only:
{{
 "title": "",
 "description": "",
 "keywords": []
}}

Rules:
- Keywords max 50
- No brand names
- SEO friendly
"""

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return eval(response.choices[0].message.content)

# ===============================
# UI
# ===============================
st.title("🚀 Microstock Metadata Generator (STABLE)")
st.caption("Color detection lokal + AI metadata (NO vision error)")

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
        st.write(", ".join(data["keywords"]))

        results.append({
            "Filename": f.name,
            "Title": data["title"],
            "Description": data["description"],
            "Keywords": ", ".join(data["keywords"])
        })

# ===============================
# CSV EXPORT
# ===============================
if results:
    df = pd.DataFrame(results)
    st.divider()
    st.subheader("📦 Adobe Stock CSV")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download CSV",
        csv,
        "adobe_stock_metadata.csv",
        "text/csv"
    )
