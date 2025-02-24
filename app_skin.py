# takes all logic and code this is main streamlit file nd we will import necessary lib
import streamlit as st
from pathlib import Path
import google.generativeai as genai


from api_key import api_keys

#configure genai with api key
genai.configure(api_key=api_keys)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}


safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]


system_prompts="""
Analyze the uploaded image to detect the skin type based on visible characteristics such as oiliness, dryness, redness, acne, pigmentation, and sensitivity. Identify the skin type from the following categories: oily, dry, combination, normal, or sensitive. Based on the detected skin type, recommend suitable skincare products including: serum, moisturizer, and sunscreen. Also, provide a list of beneficial ingredients and elements that should be included in the products for effective skincare. Additionally, mention any harmful ingredients that should be avoided based on the skin type. Ensure that the recommendations are personalized and backed by dermatological knowledge."""


model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


 # designing frontend
 # set the page configuration
st.set_page_config(page_title='Medical suggestion', page_icon=':robot:')

st.image('1.png', width=150)
st.title("Medical Center")

# set subtitle
st.subheader("help user to identify the diseases")
uploaded_file= st.file_uploader("Upload an image for your Treatment", type=['png','jpg','jpeg'])
if uploaded_file:
    st.image(uploaded_file,width=300,caption='uploaded iimage')


submit_button= st.button("Generate the Analysis")

if submit_button:
    image_data = uploaded_file.getvalue()
    # For making our image ready
    image_parts = [{
        "mime_type": "image/jpg",
        "data": image_data
    }]

# making our prompt ready
prompt_parts = [
    "Describe what happening in this image:\n",
    str(uploaded_file),  # Use the uploaded file name directly
    system_prompts,
]



# want to generate the response based on prompt and image
response = model.generate_content(prompt_parts)
st.write(response.text)
