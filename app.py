import streamlit as st
from PIL import Image
from colorthief import ColorThief

st.set_page_config(page_title="Microstock Metadata Generator", layout="centered")

st.title("🎨 Microstock Metadata Generator")
st.write("Upload image → Get Title, Description & 50 Keywords")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

def detect_color(rgb):
    r, g, b = rgb
    if b > r and b > g:
        return "blue"
    elif g > r and g > b:
        return "green"
    elif r > b and r > g:
        return "red"
    else:
        return "dark"

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)

    color_thief = ColorThief(uploaded_file)
    dominant_color = color_thief.get_color(quality=1)
    color_name = detect_color(dominant_color)

    title = f"Abstract {color_name.capitalize()} Technology Background with Gradient Shapes"

    description = (
        f"Modern abstract technology background featuring smooth gradient shapes "
        f"in {color_name} tones. Clean and dynamic design suitable for technology "
        f"concepts, digital innovation, websites, mobile applications, "
        f"presentations, banners, UI design, and corporate branding."
    )

    keywords = [
        "abstract", "background", "abstract background", "technology",
        f"{color_name} background", "gradient", "modern", "digital", "wave",
        "circles", "abstract design", "technology background", "blue gradient",
        "geometric", "shapes", "fluid", "flow", "smooth", "futuristic",
        "creative", "minimal", "clean", "corporate", "business", "innovation",
        "ui", "ux", "interface", "website background", "app background",
        "presentation", "banner", "poster", "wallpaper", "digital background",
        "modern background", "tech", "startup", "social media", "marketing",
        "design template", "dynamic", "contemporary", "gradient background",
        "technology design"
    ]

    st.subheader("📌 Title")
    st.code(title)

    st.subheader("📝 Description")
    st.write(description)

    st.subheader("🏷️ 50 Keywords")
    st.code(", ".join(keywords))
