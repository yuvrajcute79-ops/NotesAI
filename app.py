import streamlit as st
import google.generativeai as genai
from PIL import Image
import random 
import time   
from datetime import datetime
import pandas as pd # For the new Study Analytics feature

# 1. API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets!")

# --- DATABASE SIMULATION (The Market-Ready 10%) ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_minutes' not in st.session_state:
    st.session_state.total_minutes = 0
if 'credits' not in st.session_state:
    st.session_state.credits = 10 # Market-ready credit system

try:
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception:
    model = genai.GenerativeModel('gemini-1.5-flash')

# 2. UI Styling
st.set_page_config(page_title="NotesAI Pro | Market Ready", layout="wide", page_icon="🎓")

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
        background: rgba(0, 35, 102, 0.05);
        border-radius: 25px;
        padding: 30px;
        margin: 20px 0;
        border: 3px dashed #002366;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: USER ACCOUNT & ANALYTICS ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg", use_container_width=True)
    st.title("👤 Student Portal")
    st.write(f"**Account:** Premium Trial")
    st.write(f"**AI Credits Remaining:** {st.session_state.credits}")
    
    mode = st.selectbox("🎯 DASHBOARD", ["Tutor Chat", "Note Scanner", "Exam Prep", "Study Analytics"])
    
    st.divider()
    
    # PRODUCTIVITY TRACKER
    st.subheader("📈 Daily Mission")
    target_mins = st.number_input("Target (Mins)", min_value=1, value=60)
    st.progress(min(st.session_state.total_minutes / target_mins, 1.0))
    st.caption(f"Status: {st.session_state.total_minutes}/{target_mins} mins completed")

    # TIMER
    st.divider()
    t_mins = st.number_input("Focus Interval", 1, 120, 25)
    if st.button("🚀 START FOCUS"):
        t_secs = t_mins * 60
        t_display = st.empty()
        while t_secs > 0:
            mm, ss = divmod(t_secs, 60)
            t_display.markdown(f'<div class="timer-box">{mm:02d}:{ss:02d}</div>', unsafe_allow_html=True)
            time.sleep(1)
            t_secs -= 1
        st.session_state.total_minutes += t_mins
        st.balloons()
        st.rerun()

# --- MAIN INTERFACE ---
head_cols = st.columns([1, 5])
with head_cols[0]:
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=110)
with head_cols[1]:
    st.title("NotesAI Pro")
    st.write(f"Infrastructure: **Enterprise Grade** | 📅 {datetime.now().strftime('%d %b %Y')}")

# 3. MODE LOGIC

if mode == "Tutor Chat":
    st.markdown("## 💬 Neural Subject Specialist")
    subj = st.radio("Core:", ["General", "Science", "History", "Math", "English", "Economics"], horizontal=True)
    c_input = st.chat_input(f"Consult the {subj} expert...")
    
    if c_input:
        if st.session_state.credits > 0:
            st.session_state.credits -= 1
            with st.spinner("Synthesizing..."):
                resp = model.generate_content(f"You are a specialist {subj} tutor. Explain: {c_input}")
                st.session_state.history.append({"q": c_input, "a": resp.text, "type": "Chat"})
                with st.chat_message("assistant", avatar="🎓"):
                    st.write(resp.text)
        else:
            st.error("❌ Out of Credits! Please upgrade to NotesAI Gold.")

elif mode == "Note Scanner":
    st.markdown("## 📸 Vision Analysis")
    up_file = st.file_uploader("📂 Input Document", type=["jpg", "png", "jpeg"])
    
    if up_file:
        img = Image.open(up_file)
        c1, c2 = st.columns(2)
        with c1: st.image(img, use_container_width=True)
        with c2:
            if st.button("✨ ANALYZE"):
                if st.session_state.credits >= 2:
                    st.session_state.credits -= 2
                    r = model.generate_content(["Transcribe and summarize these notes.", img])
                    st.session_state.history.append({"q": "Note Scan", "a": r.text, "type": "Scan"})
                    st.write(r.text)
                else:
                    st.error("Scanner requires 2 credits.")

elif mode == "Exam Prep":
    st.markdown("## 📝 Assessment Engine")
    topic = st.text_input("Assessment Topic:")
    if st.button("🔥 GENERATE"):
        r = model.generate_content(f"Create a 5-question quiz on {topic}")
        st.write(r.text)

elif mode == "Study Analytics":
    st.markdown("## 📊 Personal Growth Tracking")
    
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.write("### Recent Activity Log")
        st.table(df[['type', 'q']])
        st.metric("Total Focus Minutes", f"{st.session_state.total_minutes}m")
    else:
        st.info("No study data logged yet. Start a session to see analytics!")

st.divider()
st.caption("NotesAI Pro v5.0 | Market-Ready Prototype | © 2026 STEM Excellence")
