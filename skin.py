import streamlit as st
import google.generativeai as genai
from api_key_for_skin import api_key_skin  # Ensure this file contains your API key
from PIL import Image
import io

# Configure GenAI with API Key
genai.configure(api_key=api_key_skin)

# Set up the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompt = (
    "Analyze the uploaded image to detect the specific skin type shown. "
    "Provide a detailed analysis of visible characteristics such as oiliness, dryness, redness, acne, pigmentation, and sensitivity. "
    "Identify the most relevant skin type from the following: oily, dry, combination, normal, or sensitive. "
    "Based on the detected skin type, provide a **personalized** skincare routine including **serum, moisturizer, and sunscreen** recommendations. "
    "List **beneficial** and **harmful** ingredients specific to the detected skin type. "
    "Ensure the response is **tailored to the individual in the image** and avoid generalizing across all skin types."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Streamlit UI Setup
st.set_page_config(page_title='Skin Type Analyzer', page_icon=':sparkles:', layout='wide')
st.image('Screenshot 2025-02-21 202250.png', width=100)
st.title("Skin Type & Skincare Recommendations")

# File Uploader
uploaded_file = st.file_uploader("Upload a skin image", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.markdown("### Uploaded Image")
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', width=300)

    # Convert image to bytes
    image_bytes = io.BytesIO()
    
    # Fix: Convert RGBA to RGB before saving as JPEG
    if image.mode == "RGBA":
        image = image.convert("RGB")
    
    image.save(image_bytes, format='JPEG')
    image_data = image_bytes.getvalue()

    # Display button and analysis results only if an image is uploaded
    if st.button("Analyze Skin & Get Recommendations"):
        with st.spinner("Analyzing... Please wait"):
            try:
                # Correctly formatting image data
                image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
                
                # Generate content using multimodal format
                response = model.generate_content([system_prompt] + image_parts, stream=False)
                response.resolve()  # Ensure the response is fully processed
                
                if hasattr(response, "text"):
                    st.subheader("🔍 Personalized Analysis Result")
                    st.markdown(response.text)
                else:
                    st.error("⚠️ Unable to analyze the image. Please try again with a clearer image.")
            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")
