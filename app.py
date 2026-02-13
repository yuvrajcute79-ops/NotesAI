import streamlit as st
import google.generativeai as genai
from PIL import Image
import random 
import time   
from datetime import datetime

# 1. API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets!")

# --- MODEL SELECTION ---
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception:
    model = genai.GenerativeModel('gemini-1.5-flash')

# 2. UI Styling & Configuration
st.set_page_config(page_title="NotesAI Pro", layout="wide", page_icon="🎓")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div.stButton > button:first-child {
        background-color: #002366;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #004080;
        color: #ffcc00;
        transform: scale(1.02);
    }
    .feature-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #002366;
    }
    .timer-box {
        font-size: 40px;
        font-weight: bold;
        color: #002366;
        text-align: center;
        background: #e0eafc;
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg", use_container_width=True)
    st.header("📌 Navigation")
    mode = st.selectbox("Choose a Study Mode", ["Tutor Chat", "Note Scanner", "Exam Prep (Quiz)"])
    
    st.divider()
    
    # FOCUS TIMER
    st.subheader("⏱️ Focus Chronometer")
    timer_minutes = st.number_input("Set Timer (mins)", min_value=1, max_value=120, value=25)
    
    if st.button("🚀 Start Timer"):
        t_seconds = timer_minutes * 60
        timer_display = st.empty()
        while t_seconds > 0:
            mins, secs = divmod(t_seconds, 60)
            timer_display.markdown(f'<div class="timer-box">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
            time.sleep(1)
            t_seconds -= 1
        st.balloons()
        st.success("Time's Up! Take a break.")

# --- MAIN CONTENT ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=100)
with col2:
    st.title("NotesAI Pro")
    st.subheader("Your Intelligent Academic Study Partner")

st.markdown("""
<div class="feature-card">
    <strong>Universal Syllabus Support:</strong> Designed to bridge the gap between 
    analog handwritten notes and digital mastery.
</div>
""", unsafe_allow_html=True)

st.divider()

# --- MODE LOGIC ---

if mode == "Tutor Chat":
    st.markdown("### 💬 Interactive Tutor")
    subject = st.radio("Focus Area:", ["General", "Science", "History", "Math", "English"], horizontal=True)
    
    chat_input = st.chat_input(f"Ask your {subject} question...")
    if chat_input:
        with st.spinner(f"NotesAI is analyzing..."):
            try:
                prompt = f"You are NotesAI, a specialist {subject} tutor for an 8th grader. Explain: {chat_input}"
                response = model.generate_content(prompt)
                with st.chat_message("assistant", avatar="🎓"):
                    st.write(response.text)
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ **System Busy:** Rate limit reached. Please wait a moment before trying again.")
                else:
                    st.error(f"Error: {e}")

elif mode == "Note Scanner":
    st.markdown("### 📸 Vision Scanner")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        img_col, text_col = st.columns(2)
        with img_col:
            st.image(img, caption='Uploaded Notes', use_container_width=True)
        
        with text_col:
            if st.button("✨ Analyze & Summarize"):
                with st.spinner("Extracting key concepts..."):
                    try:
                        response = model.generate_content(["Provide a structured summary of these notes.", img])
                        st.success("Extraction Complete!")
                        st.write(response.text)
                    except Exception as e:
                        if "429" in str(e):
                            st.warning("⚠️ **API Limit:** System is busy. Please retry in 60 seconds.")
                        else:
                            st.error(f"Error: {e}")

elif mode == "Exam Prep (Quiz)":
    st.markdown("### 📝 Quiz Generator")
    topic = st.text_input("Topic for practice quiz:")
    
    if st.button("🔥 Generate Practice Quiz"):
        with st.spinner("Architecting test..."):
            try:
                response = model.generate_content(f"Generate a 5-question MCQ quiz on {topic} for an 8th grader. Include answers.")
                st.balloons() 
                st.write(response.text)
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ **Quota Reached:** Please wait a minute before generating another quiz.")
                else:
                    st.error(f"Error: {e}")

st.divider()
st.caption("NotesAI Pro | Concept by Parth | Developed by Yuvraj | © 2026 STEM Excellence")
