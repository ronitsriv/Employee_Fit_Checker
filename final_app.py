import streamlit as st
import pandas as pd
import google.generativeai as genai

# -------------------------------
# Configure Gemini API
# -------------------------------
API_KEY = "your-api-key-here"   # replace with your key or I will put temp one soon
genai.configure(api_key=API_KEY)

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Lead Scoring AI App")
st.write(
    "This app uses simple rules and Gemini AI to classify lead intent. "
    "Basic AI model parameters are exposed to understand how they affect responses."
)

# -------------------------------
# AI Model Settings (Learning)
# -------------------------------
st.subheader("AI Model Settings (Learning)")

st.caption(
    "These settings help understand how AI models behave. "
    "Try changing them and observe how the response changes."
)

temperature = st.slider(
    "Temperature (Creativity)",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.1,
    help="Lower values make responses more strict and predictable. "
         "Higher values make responses more creative."
)

max_tokens = st.slider(
    "Max Output Tokens",
    min_value=64,
    max_value=512,
    value=256,
    step=64,
    help="Controls how long the AI response can be."
)

model_name = st.selectbox(
    "Gemini Model",
    ["models/gemini-2.5-flash"],
    help="Flash model is fast and suitable for classification tasks."
)

# -------------------------------
# Lead Input
# -------------------------------
st.subheader("Lead Details")

lead_text = st.text_area(
    "Enter lead information",
    placeholder="Example: Head of Growth at B2B SaaS company. Scaling GTM team.",
    height=120
)

# -------------------------------
# Run AI Scoring
# -------------------------------
if st.button("Classify Lead Intent"):

    if not lead_text.strip():
        st.warning("Please enter lead details.")
    else:
        model = genai.GenerativeModel(model_name)

        prompt = f"""
        Classify the following lead as High, Medium, or Low intent.

        Lead details:
        {lead_text}

        Give a short reason for the classification.
        """

        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens
        }

        with st.spinner("Analyzing lead..."):
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )

        st.subheader("AI Response")
        st.write(response.text)
