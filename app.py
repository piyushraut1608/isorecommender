import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env if available
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("GEMINI_API_KEY not found in environment variables.")

# Streamlit UI setup
st.set_page_config(page_title="ISO 27001:2022 Recommender", layout="centered")
st.title("🔐 ISO 27001:2022 Control Recommender")
st.markdown("Provide your organization context to receive tailored ISO control recommendations.")

with st.form("context_form"):
    industry = st.text_input("Industry", placeholder="e.g., Fintech, Healthcare")
    sensitivity = st.selectbox("Data Sensitivity", ["Low", "Medium", "High"])
    risks = st.text_area("Key Risks (comma-separated)", placeholder="e.g., insider threat, phishing, cloud misconfig")
    gaps = st.text_area("Known Gaps or Audit Findings", placeholder="e.g., no vendor risk management, no endpoint protection")
    maturity = st.selectbox("Maturity Level", ["Basic", "Intermediate", "Advanced"])
    submitted = st.form_submit_button("Get Recommendations")

if submitted:
    if not api_key:
        st.stop()

    st.info("Generating recommendations with Gemini 2.0 Flash...")

    # Construct the prompt
    prompt = f"""
    You are an ISO 27001:2022 compliance assistant.

    Given the following organization profile, recommend 3–5 relevant ISO 27001:2022 Annex A controls. For each, explain why it applies and suggest one concrete implementation step.

    Context:
    Industry: {industry}
    Data Sensitivity: {sensitivity}
    Key Risks: {risks}
    Gaps: {gaps}
    Maturity Level: {maturity}

    Respond in the following section-wise text-block format, one section text block followed by another:
    1. Control ID – Control Title
       • Section 1 - Why it's relevant
       • Section 2 - Suggested action
       • Section 3 - Available controls that are best fit, also mention any vendors or products that are best in market.

    Display in the following format, separate text-block for each section, each section shall have its own bullet point:
    1. Control ID – Control Title
    • Section 1 -Why it's relevant
       • Section 2 - Suggested action
       • Section 3 - Available controls that are best fit
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        st.subheader("📋 Recommended Controls")
        st.markdown(response.text.strip())
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
