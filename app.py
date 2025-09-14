import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ No Gemini API key found. Set GEMINI_API_KEY in .env or Streamlit secrets.")
else:
    genai.configure(api_key=API_KEY)
    # ✅ Correct way: create model object directly
    model = genai.GenerativeModel("gemini-1.5-flash")

def summarize_text(text: str, max_output_tokens: int = 512) -> str:
    """Summarize text using Gemini 1.5-flash."""
    prompt = (
        "Summarize the following text into concise bullet points and a 2–3 sentence overall summary.\n\n"
        f"{text}"
    )
    # ✅ Correct usage
    response = model.generate_content(
        prompt,
        generation_config={"max_output_tokens": max_output_tokens, "temperature": 0.0},
    )
    return getattr(response, "text", str(response))

# --- Streamlit UI ---
st.set_page_config(page_title="Gemini 1.5-flash Summarizer", layout="centered")
st.title("📄 Document Summarizer by Ai")

st.markdown("Paste your text or upload a .txt file. The app will generate a concise summary.")

uploaded = st.file_uploader("Upload a .txt file", type=["txt"])
if uploaded is not None:
    raw_text = uploaded.read().decode("utf-8")
else:
    raw_text = st.text_area("Paste your text here", height=250)

if st.button("Summarize") and raw_text.strip():
    with st.spinner("Summarizing with Gemini 1.5-flash..."):
        try:
            summary = summarize_text(raw_text)
            st.subheader("✅ Summary")
            st.markdown(summary)
            st.download_button("Download summary", summary, file_name="summary.txt", mime="text/plain")
        except Exception as e:
            st.error(f"Error: {e}")