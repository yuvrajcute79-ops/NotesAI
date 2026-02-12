import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
# On Streamlit Cloud, set this in Settings > Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    # For local testing - replace with your key if running on your laptop
    genai.configure(api_key="PASTE_YOUR_KEY_HERE")

model = genai.GenerativeModel('gemini-1.5-flash')

# 2. UI Styling (NMWS Colors: Navy & Gold vibe)
st.set_page_config(page_title="AI Study Lab", layout="wide")

# FIXED LINE BELOW: Changed unsafe_allow_globals to unsafe_allow_html
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
            response = model.generate_content(f"You are a helpful academic tutor. Explain this clearly for an 8th grader: {chat_input}")
            st.chat_message("assistant").write(response.text)

elif mode == "Note Scanner":
    st.info("Upload a photo of your handwritten notes or textbook.")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption='Notes Detected', width=300)
        if st.button("Analyze & Summarize"):
            with st.spinner("AI is reading your handwriting..."):
                response = model.generate_content(["Read this image. Transcribe the text and provide a structured summary with key points.", img])
                st.markdown("### 📝 AI Summary")
                st.write(response.text)

elif mode == "Exam Prep (Quiz)":
    st.info("Enter a topic to generate a practice quiz.")
    topic = st.text_input("Enter Topic (e.g., '1857 Revolt' or 'Organic Chemistry')")
    if st.button("Generate 5-Question Quiz"):
        with st.spinner("Creating your quiz..."):
            response = model.generate_content(f"Generate a 5-question multiple choice quiz on {topic} for an 8th-grade student. Include answers at the end.")
            st.markdown("### ❓ Practice Quiz")
            st.write(response.text)
