import streamlit as st
from PIL import Image
import base64
import json
import pandas as pd
from openai import OpenAI

# ================= CONFIG =================
st.set_page_config(
    page_title="Adobe Stock Metadata Generator",
    page_icon="📦",
    layout="centered"
)

st.title("📦 Adobe Stock Metadata Generator (Batch + AI)")
st.caption("Upload images → AI generates Title, Description & Keywords → CSV Ready")

# ================= API =================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ================= AI VISION =================
def analyze_image_ai(image):
    buffered = image.convert("RGB")
    img_bytes = buffered.tobytes()
    encoded = base64.b64encode(img_bytes).decode()

    prompt = """
You are a professional Adobe Stock metadata editor.

Analyze the image and return ONLY valid JSON:

{
  "main_color": "",
  "secondary_colors": [],
  "shapes": [],
  "style": [],
  "mood": [],
  "best_use": []
}

Rules:
- Colors: simple English (blue, purple, green, etc)
- Shapes: wave, circle, mesh, line, abstract shapes
- Style: gradient, fluid, minimal, futuristic, digital
- Best_use: website background, app background, presentation, branding
- Do NOT add explanations
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_base64", "image_base64": encoded}
                ]
            }
        ],
        max_tokens=300
    )

    return json.loads(response.choices[0].message.content)

# ================= METADATA =================
def build_metadata(ai):
    color = ai["main_color"] or "abstract"
    shape = ai["shapes"][0] if ai["shapes"] else "abstract shapes"
    style = ai["style"][0] if ai["style"] else "modern"

    titles = [
        f"Abstract {color.capitalize()} {shape} Technology Background",
        f"Modern {color.capitalize()} Gradient {shape}",
        f"Futuristic {color.capitalize()} Abstract Digital Background",
        f"{color.capitalize()} {shape} Design for Technology",
        f"Abstract {color.capitalize()} Background with {shape}"
    ]

    description = (
        f"Modern abstract background featuring {shape} with {style} style "
        f"in {color} color tones. Suitable for "
        f"{', '.join(ai['best_use']) if ai['best_use'] else 'technology projects'}, "
        f"websites, mobile applications, presentations, branding, "
        f"and digital marketing."
    )

    keywords = list(dict.fromkeys(
        [
            "abstract background",
            f"{color} background",
            "technology background",
            "gradient background",
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
            "visual design"
        ]
        + ai["shapes"]
        + ai["style"]
        + ai["best_use"]
    ))[:50]

    return titles[0], description, keywords

# ================= UI =================
uploaded_files = st.file_uploader(
    "Upload Images (Batch)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

rows = []

if uploaded_files:
    with st.spinner("Analyzing images with AI..."):
        for file in uploaded_files:
            image = Image.open(file)

            ai_data = analyze_image_ai(image)
            title, description, keywords = build_metadata(ai_data)

            rows.append({
                "Filename": file.name,
                "Title": title,
                "Description": description,
                "Keywords": ", ".join(keywords)
            })

    df = pd.DataFrame(rows, columns=[
        "Filename", "Title", "Description", "Keywords"
    ])

    st.success(f"{len(rows)} files ready for Adobe Stock")

    st.dataframe(df)

    st.download_button(
        "⬇️ Download Adobe Stock CSV (Batch)",
        df.to_csv(index=False),
        "adobe_stock_batch.csv",
        mime="text/csv"
    )
