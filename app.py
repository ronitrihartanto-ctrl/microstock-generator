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

# ===============================
# API KEY CHECK (PENTING)
# ===============================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY belum diset di Streamlit Secrets")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]

# ===============================
# UTILS
# ===============================
def image_to_base64(img: Image.Image) -> str:
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# ===============================
# AI ANALYSIS (VISION)
# ===============================
def analyze_image_ai(img: Image.Image):
    image_base64 = image_to_base64(img)

    prompt = """
You are a professional Adobe Stock metadata expert.

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
- Colors: simple English (blue, purple, green, red, orange, yellow, black, white, gray, pink, teal, cyan)
- Shapes: wave, circle, curve, line, mesh, abstract
- Style: gradient, minimal, modern, futuristic, digital, smooth
- Best_use: website background, app background, presentation, branding, wallpaper
- NO explanation text
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an Adobe Stock metadata specialist."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=400
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except openai.error.AuthenticationError:
        st.error("❌ API key OpenAI tidak valid / billing belum aktif")
        st.stop()

    except Exception as e:
        st.error("❌ Gagal menganalisis gambar dengan AI")
        st.caption(str(e))
        return None

# ===============================
# METADATA GENERATOR
# ===============================
def generate_metadata(data):
    main_color = data.get("main_color", "abstract")
    shapes = ", ".join(data.get("shapes", [])[:2])
    style = ", ".join(data.get("style", [])[:2])
    best_use = ", ".join(data.get("best_use", [])[:2])

    title = f"Abstract {main_color.capitalize()} Background with {shapes}"

    description = (
        f"High quality abstract {main_color} background featuring {shapes}. "
        f"Modern {style} style suitable for {best_use}. "
        "Perfect for website backgrounds, presentations, digital design and branding."
    )

    keywords = [
        main_color,
        "abstract background",
        *data.get("secondary_colors", []),
        *data.get("shapes", []),
        *data.get("style", []),
        *data.get("mood", []),
        *data.get("best_use", []),
        "modern",
        "digital",
        "design",
        "wallpaper",
        "technology",
        "creative",
        "art",
        "template",
        "backdrop"
    ]

    keywords = list(dict.fromkeys([k for k in keywords if k]))[:50]

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
            analysis = analyze_image_ai(img)

            if not analysis:
                continue

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
        "⬇️ Download CSV (Adobe Stock)",
        csv,
        "adobe_stock_metadata.csv",
        "text/csv"
    )
