import streamlit as st
from PIL import Image
from google import genai
import os
from dotenv import load_dotenv

# -----------------------
# Step 1: Load API key
# -----------------------
load_dotenv()

# -----------------------
# Step 2: Function to get AI response
# -----------------------
def get_gemini_response(input_text, image, prompt):

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            input_text or "",
            image,   # ✅ directly pass PIL image
            prompt
        ]
    )

    return response.text


# -----------------------
# Step 3: Streamlit UI
# -----------------------
st.set_page_config(page_title="AI Civil Engineering Image Analyzer")
st.header("🏗 AI Civil Engineering Image Analyzer")

input_text = st.text_input("Enter additional description (optional)", "")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)


# -----------------------
# Step 4: AI Prompt
# -----------------------
input_prompt = """
You are a civil engineer. Analyze the structure in the image and provide:

1. Type of Structure
2. Materials Used
3. Structural Components
4. Possible Structural Issues
5. Additional Observations
"""


# -----------------------
# Step 5: Analyze Button
# -----------------------
if st.button("Analyze Image"):

    if image is not None:

        try:
            with st.spinner("Analyzing structure... Please wait"):
                response = get_gemini_response(
                    input_text,
                    image,
                    input_prompt
                )

            st.subheader("Analysis Result")
            st.markdown(response)

        except Exception as e:
            st.error(f"Error: {str(e)}")

    else:
        st.warning("Please upload an image first.")
