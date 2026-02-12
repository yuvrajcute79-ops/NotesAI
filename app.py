import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets!")

# --- MODEL SELECTION (February 2026 Update) ---
# We use gemini-2.5-flash as the primary stable model.
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    # Quick test to see if the model name exists
    model.generate_content("test", generation_config={"max_output_tokens": 1})
except Exception:
    # Fallback to the latest Preview if 2.5 is unavailable in your region
    model = genai.GenerativeModel('gemini-3-flash-preview')

# 2. UI Styling (NMWS Colors: Navy & Gold)
st.set_page_config(page_title="AI Study Lab", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div.stButton > button:first-child {
        background-color: #002366;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Universal AI Study Companion")
st.sidebar.header("Navigation")
mode = st.sidebar.selectbox("Choose a Study Mode", ["Tutor Chat", "Note Scanner", "Exam Prep (Quiz)"])

# 3. Mode Logic
if mode == "Tutor Chat":
    st.info("Ask me anything about History, Chemistry, Math, or Physics!")
    chat_input = st.chat_input("Type your question here...")
    if chat_input:
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(f"You are a helpful academic tutor. Explain this clearly for an 8th grader: {chat_input}")
                st.chat_message("assistant").write(response.text)
            except Exception as e:
                st.error(f"AI Error: {e}")

elif mode == "Note Scanner":
    st.info("Upload a photo of your handwritten notes.")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption='Notes Detected', width=300)
        if st.button("Analyze & Summarize"):
            with st.spinner("AI is reading your handwriting..."):
                try:
                    response = model.generate_content(["Read this image. Transcribe the text and provide a structured summary with key points.", img])
                    st.markdown("### 📝 AI Summary")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

elif mode == "Exam Prep (Quiz)":
    st.info("Enter a topic to generate a practice quiz.")
    topic = st.text_input("Enter Topic (e.g., '1857 Revolt')")
    if st.button("Generate 5-Question Quiz"):
        with st.spinner("Creating your quiz..."):
            try:
                response = model.generate_content(f"Generate a 5-question multiple choice quiz on {topic} for an 8th-grade student. Include answers at the end.")
                st.markdown("### ❓ Practice Quiz")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI Error: {e}")
