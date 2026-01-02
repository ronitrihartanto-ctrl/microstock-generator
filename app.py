import streamlit as st
import openai
import base64
import json
import pandas as pd
from PIL import Image
from io import BytesIO

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Microstock Metadata Generator", layout="wide")
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ===============================
# FUNCTIONS
# ===============================

def image_to_base64(img: Image.Image) -> str:
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def analyze_image_ai(img: Image.Image):
    image_base64 = image_to_base64(img)

    prompt = """
You are a professional Adobe Stock metadata expert.

Analyze the image and return ONLY valid JSON with this structure:

{
  "main_color": "",
  "secondary_colors": [],
  "shapes": [],
  "style": [],
  "mood": [],
  "best_use": []
}

Rules:
- Colors must be common English colors (blue, purple, green, red, orange, yellow, black, white, gray, pink, teal, cyan)
- Shapes: wave, circle, curve, line, mesh, abstract
- Style: gradient, minimal, modern, futuristic, digital, smooth
- Best_use: website background, app background, presentation, branding, wallpaper
- NO explanation text
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an Adobe Stock metadata specialist."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_base64", "image_base64": image_base64}
                ]
            }
        ],
        max_tokens=300
    )

    return json.loads(response.choices[0].message.content)

def generate_metadata(data):
    main_color = data["main_color"]
    style = ", ".join(data["style"][:2])
    shapes = ", ".join(data["shapes"][:2])

    title = f"Abstract {main_color.capitalize()} Background with {shapes}"
    description = (
        f"High quality abstract {main_color} background featuring {shapes}. "
        f"Modern {style} style suitable for {', '.join(data['best_use'][:2])}. "
        "Perfect for digital design, web backgrounds, presentations and branding."
    )

    keywords = [
        main_color,
        "abstract background",
        *data["secondary_colors"],
        *data["shapes"],
        *data["style"],
        *data["mood"],
        *data["best_use"],
        "digital",
        "modern",
        "design",
        "wallpaper",
        "technology",
        "creative",
        "art",
        "template",
        "backdrop"
    ]

    # Bersihkan & limit 50 keyword
    keywords = list(dict.fromkeys(keywords))[:50]

    return title, description, keywords

# ===============================
# UI
# ===============================

st.title("🚀 Microstock Metadata Generator (Adobe Stock)")
st.caption("Upload image → AI generates title, description & 50 keywords")

uploaded_files = st.file_uploader(
    "Upload image(s)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

results = []

if uploaded_files:
    for file in uploaded_files:
        st.divider()
        img = Image.open(file).convert("RGB")
        st.image(img, width=300)

        with st.spinner("Analyzing image with AI..."):
            try:
                analysis = analyze_image_ai(img)
                title, desc, keywords = generate_metadata(analysis)

                st.subheader("Title")
                st.write(title)

                st.subheader("Description")
                st.write(desc)

                st.subheader("Keywords (50)")
                st.write(", ".join(keywords))

                results.append({
                    "Filename": file.name,
                    "Title": title,
                    "Description": desc,
                    "Keywords": ", ".join(keywords)
                })

            except Exception as e:
                st.error("AI analysis failed. Try again.")

# ===============================
# CSV EXPORT
# ===============================
if results:
    st.divider()
    df = pd.DataFrame(results)

    st.subheader("📦 Adobe Stock CSV Export")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download CSV (Adobe Stock)",
        csv,
        "adobe_stock_metadata.csv",
        "text/csv"
    )
