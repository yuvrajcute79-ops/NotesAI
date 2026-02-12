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
    model = genai.GenerativeModel('gemini-2.5-flash')
    model.generate_content("test", generation_config={"max_output_tokens": 1})
except Exception:
    model = genai.GenerativeModel('gemini-3-flash-preview')

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
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button:hover {
        background-color: #004080;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
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
        font-family: 'Courier New', Courier, monospace;
    }
    .stat-text {
        font-size: 0.9rem;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: PRO DASHBOARD ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg", use_container_width=True)
    st.title("🚀 NotesAI Pro")
    
    mode = st.selectbox("🎯 SELECT CAPABILITY", ["Tutor Chat", "Note Scanner", "Exam Prep (Quiz)"])
    
    st.divider()
    
    # ADVANCED GOAL TRACKER
    st.subheader("📈 Productivity Tracker")
    target_mins = st.number_input("Daily Mission (Mins)", min_value=1, max_value=720, value=60)
    completed_mins = st.slider("Progress Verified", 0, target_mins, int(target_mins*0.4))
    
    prog = (completed_mins / target_mins)
    st.progress(prog)
    
    cols = st.columns(2)
    cols[0].metric("Efficiency", f"{int(prog*100)}%")
    cols[1].metric("Streak", "5 Days", "🔥")

    if prog >= 1.0:
        st.success("🏆 DAILY GOAL ACHIEVED!")
    elif prog >= 0.5:
        st.info("⚡ Halfway to Greatness!")

    # LIVE TICKING TIMER
    st.divider()
    st.subheader("⏱️ Deep Work Timer")
    t_mins = st.number_input("Focus Period", 1, 120, 25)
    
    if st.button("🔥 INITIATE SESSION"):
        t_secs = t_mins * 60
        t_display = st.empty()
        while t_secs > 0:
            mm, ss = divmod(t_secs, 60)
            t_display.markdown(f'<div class="timer-box">{mm:02d}:{ss:02d}</div>', unsafe_allow_html=True)
            time.sleep(1)
            t_secs -= 1
        t_display.balloons()
        st.success("Session Logged! Reward: +50 XP")

# --- MAIN INTERFACE ---
head_cols = st.columns([1, 5])
with head_cols[0]:
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=110)
with head_cols[1]:
    st.title("NotesAI: The Universal Learning Engine")
    st.write(f"📅 {datetime.now().strftime('%A, %B %d, %Y')} | 👤 Account: Scholar-User")

st.markdown("""
<div class="feature-card">
    <h3>🌐 Global Academic Support</h3>
    NotesAI is your high-performance bridge between analog study and digital mastery. 
    Our neural engine deciphers complex handwriting, simplifies multi-domain concepts, 
    and validates your expertise through adaptive assessments. <strong>Unrestricted grade support active.</strong>
</div>
""", unsafe_allow_html=True)

# DYNAMIC STUDY TIPS
tips = [
    "🧠 **Active Recall:** Cover your notes and try to state the facts from memory.",
    "🍅 **Pomodoro Technique:** Work for 25 mins, rest for 5 to keep the brain fresh.",
    "🔗 **Interleaving:** Mix different subjects in one session to improve problem-solving.",
    "✍️ **Feynman Method:** Explain a concept to a 5-year-old to find your weak spots."
]
st.info(random.choice(tips))

st.divider()

# --- CAPABILITY LOGIC ---

if mode == "Tutor Chat":
    st.markdown("## 💬 AI Subject Specialist")
    subj = st.radio("Specialization:", ["General", "Science", "History", "Math", "English", "Physics", "Chemistry", "Economics"], horizontal=True)
    
    details = {
        "General": "Cross-domain logic and general knowledge.",
        "Science": "Biological processes and general scientific method.",
        "History": "Historiography, cause-effect analysis, and timelines.",
        "Math": "Calculus, Algebra, and Geometry visualization.",
        "English": "Linguistic analysis, literature, and rhetoric.",
        "Physics": "Kinematics, Thermodynamics, and Quantum theory.",
        "Chemistry": "Organic synthesis, Periodic trends, and Stoichiometry.",
        "Economics": "Macro/Micro dynamics and market analysis."
    }
    
    [Image of a library of academic books and a brain icon representing diverse knowledge]
    
    st.caption(f"🧠 **System Configuration:** {details[subj]} | **Support:** All Grades/Levels")
    
    c_input = st.chat_input(f"Consult the {subj} Specialist...")
    if c_input:
        with st.spinner(f"NotesAI {subj} Core is processing..."):
            try:
                p = f"You are Notes
