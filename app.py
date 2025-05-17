import streamlit as st
import google.generativeai as genai
import os
import re
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

# User input form
with st.form("context_form"):
    industry = st.text_input("Industry", placeholder="e.g., Fintech, Healthcare")
    sensitivity = st.selectbox("Data Sensitivity", ["Low", "Medium", "High"])
    risks = st.text_area("Key Risks (comma-separated)", placeholder="e.g., insider threat, phishing, cloud misconfig")
    gaps = st.text_area("Known Gaps or Audit Findings", placeholder="e.g., no vendor risk management, no endpoint protection")
    maturity = st.selectbox("Maturity Level", ["Basic", "Intermediate", "Advanced"])
    submitted = st.form_submit_button("Get Recommendations")

st.text("Made by Piyush")


def clean_title(text):
    return re.sub(r"[#*_`]", "", text).strip()

if submitted:
    if not api_key:
        st.stop()

    st.info("Generating recommendations with Gemini 2.0 Flash...")

    prompt = f"""
You are an ISO 27001:2022 compliance assistant.

Given the following organization profile, recommend 3–5 relevant ISO 27001:2022 Annex A controls. For each control, your response must strictly follow this 3-part format:

Format:
### **A.<number> – Control Title**


**• Section 1 - Why it's relevant**: Explain why this control applies to the organization’s risks and context.

**• Section 2 - Suggested action**: Describe specific and in-detailed implementation steps the organization should take to address this control.

**• Section 3 - Available controls that are best fit**: mention list of any tools, platforms, or vendors that are best in market. in bullet points. Also explain why that particular control is best fit
Only return the formatted recommendation blocks for each control, with no summaries or introductory text. Each control must follow the exact format above.

Make sure the text, bullet-points and everything is well-aligned. Also, once section 3 is completed give a horizontal line. Do not use any HTML like <div> or <hr>
Context:
Industry: {industry}  
Data Sensitivity: {sensitivity}  
Key Risks: {risks}  
Gaps: {gaps}  
Maturity Level: {maturity}
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        output = response.text.strip()

        output = response.text.strip()
        output = re.sub(r"</?div>", "", output, flags=re.IGNORECASE)
        output = re.sub(r"<hr\s*/?>", "---", output)


        st.subheader("📋 Recommended Controls as per Annexure A")

        control_blocks = re.split(r"(?=\d+\.\sA\.)", output)

        for block in control_blocks:
            if block.strip():
                lines = block.strip().split("\n", 1)
                if len(lines) == 2:
                    title_line, content = lines
                else:
                    title_line, content = lines[0], ""

                # Clean up Markdown symbols from title
                cleaned_title = clean_title(title_line)

                st.markdown(
                    f"""
<div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin-bottom: 25px; background-color: #fafafa;">
    <h4 style="font-weight: 600; margin-top: 0;">{cleaned_title}</h4>
    <div style="white-space: pre-wrap; font-family: inherit; font-size: 1rem;">
        {content}
    </div>
</div>
""",
                    unsafe_allow_html=True
                )






    except Exception as e:
     st.error(f"Error generating recommendations: {e}")
