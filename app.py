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
        border-radius: 12px;
        height: 3.5em;
        width: 100%;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #004080;
        transform: translateY(-2px);
        color: #ffcc00;
    }
    .feature-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border-left: 8px solid #002366;
    }
    .timer-box {
        font-size: 60px;
        font-weight: 800;
        color: #002366;
        text-align: center;
        background: #eef2f3;
        border-radius: 25px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid #002366;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg", use_container_width=True)
    st.title("🚀 NotesAI Pro")
    
    mode = st.selectbox("🎯 SELECT CAPABILITY", ["Tutor Chat", "Note Scanner", "Exam Prep (Quiz)"])
    st.divider()
    
    # FOCUS TIMER
    st.subheader("⏱️ Focus Chronometer")
    t_mins = st.number_input("Study Interval (Mins)", 1, 120, 25)
    
    if st.button("🔥 START FOCUS SESSION"):
        t_secs = t_mins * 60
        t_display = st.empty()
        while t_secs > 0:
            mm, ss = divmod(t_secs, 60)
            t_display.markdown(f'<div class="timer-box">{mm:02d}:{ss:02d}</div>', unsafe_allow_html=True)
            time.sleep(1)
            t_secs -= 1
        st.balloons()
        st.success("Interval Complete!")

# --- MAIN INTERFACE ---
head_cols = st.columns([1, 5])
with head_cols[0]:
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=110)
with head_cols[1]:
    st.title("NotesAI: The Universal Learning Engine")
    st.write(f"📅 {datetime.now().strftime('%A, %B %d, %Y')} | 🌍 Status: Active")

st.markdown("""
<div class="feature-card">
    <h3>🌐 Specialized Academic Intelligence</h3>
    NotesAI is a dedicated learning platform. By specializing in academic subjects, 
    it delivers more precise and safer results than general-purpose AI models.
</div>
""", unsafe_allow_html=True)

# --- CAPABILITY LOGIC ---

if mode == "Tutor Chat":
    st.markdown("## 💬 AI Subject Specialist")
    subj = st.radio("Subject Focus:", ["Science", "History", "Math", "English", "Physics", "Chemistry"], horizontal=True)
    
    # NEW FEATURE: Complexity Level
    complexity = st.select_slider("Explanation Detail:", options=["Simplified", "Standard", "Advanced"])
    
    c_input = st.chat_input(f"Consult the {subj} Specialist...")
    if c_input:
        with st.spinner(f"NotesAI is analyzing at {complexity} level..."):
            try:
                p = f"You are NotesAI, a world-class {subj} expert. Provide a {complexity} level explanation for: {c_input}"
                resp = model.generate_content(p)
                with st.chat_message("assistant", avatar="🎓"):
                    st.write(resp.text)
                    st.download_button("📥 Download Explanation", resp.text, "Explanation.txt")
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ **System Busy:** The AI is taking a quick breath. Please wait 30-60 seconds and try again.")
                else:
                    st.error(f"Error: {e}")

elif mode == "Note Scanner":
    st.markdown("## 📸 Vision Analysis Core")
    up_file = st.file_uploader("📂 Upload Handwritten Document", type=["jpg", "png", "jpeg"])
    
    if up_file:
        img = Image.open(up_file)
        st.image(img, caption='Input Stream', width=400)
        
        # NEW FEATURE: Analysis Focus
        scan_focus = st.selectbox("Scanner Focus:", ["General Summary", "Extract Formulas", "Key Definitions Only"])
        
        if st.button("✨ DEPLOY VISION SCAN"):
            with st.spinner(f"Decoding handwriting for {scan_focus}..."):
                try:
                    r = model.generate_content([f"Act as an academic OCR. Perform a {scan_focus} on these notes.", img])
                    st.markdown("### 📝 Digital Intelligence Report")
                    st.write(r.text)
                    st.download_button("📥 Save to Device", r.text, "Scanned_Notes.txt")
                except Exception as e:
                    if "429" in str(e):
                        st.warning("⚠️ **Scanner Paused:** Rate limit reached. Try again in 60 seconds.")
                    else:
                        st.error(f"Vision Error: {e}")

elif mode == "Exam Prep (Quiz)":
    st.markdown("## 📝 Adaptive Assessment Engine")
    topic = st.text_input("Define Assessment Topic:", placeholder="e.g., Cellular Respiration")
    
    # NEW FEATURE: Question Count
    q_count = st.slider("Number of Questions:", 3, 10, 5)
    
    if st.button("🔥 GENERATE ASSESSMENT"):
        with st.spinner(f"Architecting {q_count} questions..."):
            try:
                r = model.generate_content(f"Generate a {q_count}-question quiz on {topic}. Include an answer key.")
                st.balloons()
                st.write(r.text)
                st.download_button("📥 Export Quiz", r.text, "Study_Quiz.txt")
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ **Assessment Hub Overloaded:** Please wait a minute before generating a new quiz.")
                else:
                    st.error(f"Generation Failed: {e}")

st.divider()
st.caption("NotesAI Pro Framework | Concept by Parth | Developed by Yuvraj | © 2026 AI Excellence")
