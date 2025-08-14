import streamlit as st
from PIL import Image
import io

# App title
st.set_page_config(page_title="PNG to JPG Converter", page_icon="🖼️")
st.title("🖼️ PNG → JPG Converter")
st.write("Upload a PNG image, and download it as a JPG.")

# Upload file
uploaded_file = st.file_uploader("Choose a PNG file", type=["png"])

if uploaded_file:
    try:
        # Open the PNG image
        img = Image.open(uploaded_file)

        # Handle transparency (RGBA/LA)
        if img.mode in ("RGBA", "LA"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            alpha = img.split()[-1]
            bg.paste(img, mask=alpha)
            img = bg
        else:
            img = img.convert("RGB")

        # Show preview
        st.image(img, caption="Converted Image Preview", use_container_width=True)

        # Save to bytes for download
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG", quality=95)
        img_bytes.seek(0)

        # Download button
        st.download_button(
            label="📥 Download as JPG",
            data=img_bytes,
            file_name="converted.jpg",
            mime="image/jpeg"
        )

    except Exception as e:
        st.error(f"Error: {e}")
