# frontend/app.py

import streamlit as st
import requests
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Smart Summarizer", layout="centered")
load_dotenv()  # Load .env for any frontend keys later if needed

# 💡 Custom styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .title {
        color: #0e76a8;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .tagline {
        text-align: center;
        font-size: 16px;
        color: #555;
        margin-top: 0px;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 💼 Branding
st.markdown('<p class="title">📄 Smart Summarizer</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Powered by AI — Built by Branden Bryant</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📎 Upload your document", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    st.write(f"**Selected file:** `{uploaded_file.name}`")

    if st.button("✨ Summarize"):
        with st.spinner("⏳ Generating summary..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            try:
                response = requests.post("http://127.0.0.1:8000/summarize/", files=files)
                result = response.json()

                if "summary" in result:
                    summary_text = result['summary']
                    st.success("✅ Summary Generated:")
                    st.markdown(f"```{summary_text}```")

                    # Save summary to file
                    with open("summary_output.txt", "w", encoding="utf-8") as f:
                        f.write(summary_text)

                    # Download button
                    st.download_button(
                        label="💾 Download Summary as .txt",
                        data=summary_text,
                        file_name="summary.txt",
                        mime="text/plain"
                    )

                    # 💌 Email section
                    st.markdown("### 📬 Email Your Summary")
                    email = st.text_input("Enter your email address")

                    if st.button("📨 Send Summary via Email"):
                        with st.spinner("Sending..."):
                            from app.email_utils import send_summary_email
                            success = send_summary_email(email, summary_text)
                            if success:
                                st.success("✅ Summary sent successfully!")
                            else:
                                st.error("❌ Failed to send email.")
                else:
                    st.error(f"🚫 Error: {result.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"❌ Could not connect to the backend: {e}")
