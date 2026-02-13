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

# --- 2. RESTING LOGIC (Handles Quota/429 Errors) ---
def safe_ai_call(prompt_data):
    try:
        response = model.generate_content(prompt_data)
        return response.text
    except Exception as e:
        if "429" in str(e):
            st.info("😴 **NotesAI is taking a quick power nap...**")
            st.caption("The AI engine is refreshing its memory. Please wait 60 seconds.")
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.6) # 60 seconds total
                progress_bar.progress(percent_complete + 1)
            st.success("✨ AI is awake! Please click the button again.")
            return None
        else:
            st.error(f"AI Error: {e}")
            return None

# --- 3. ACCOUNT SYSTEM ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_db' not in st.session_state:
    st.session_state.user_db = {"admin": "password123"} 

def login_page():
    st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #002366;">🎓 NotesAI Pro</h1>
            <p>Please Sign In to access the Universal Learning Engine</p>
        </div>
    """, unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    with tab1:
        u_email = st.text_input("Email/Username", key="login_user")
        u_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Access Account"):
            if u_email in st.session_state.user_db and st.session_state.user_db[u_email] == u_pass:
                st.session_state.authenticated = True
                st.session_state.current_user = u_email
                st.rerun()
            else:
                st.error("Invalid credentials.")
    with tab2:
        new_user = st.text_input("Choose Username", key="reg_user")
        new_pass = st.text_input("Create Password", type="password", key="reg_pass")
        confirm_pass = st.text_input("Confirm Password", type="password")
        if st.button("Create Student Profile"):
            if new_pass == confirm_pass and new_user:
                st.session_state.user_db[new_user] = new_pass
                st.success("Account created! Login to continue.")

if not st.session_state.authenticated:
    login_page()
    st.stop()

# --- 4. UI Styling & Configuration ---
st.set_page_config(page_title="NotesAI Pro | Enterprise Education", layout="wide", page_icon="🎓")

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
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
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
    st.write(f"👤 User: **{st.session_state.current_user}**")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    mode = st.selectbox("🎯 SELECT CAPABILITY", ["Tutor Chat", "Note Scanner", "Exam Prep (Quiz)"])
    st.divider()
    
    st.subheader("📊 Session Intelligence")
    target_mins = st.number_input("Daily Mission (Mins)", min_value=1, max_value=720, value=60)
    completed_mins = st.slider("Session Progress", 0, target_mins, int(target_mins*0.4))
    st.progress(completed_mins / target_mins)
    
    st.divider()
    st.subheader("⏱️ Focus Timer")
    t_mins = st.number_input("Study Interval", 1, 120, 25)
    if st.button("🔥 START DEEP WORK"):
        t_secs = t_mins * 60
        t_display = st.empty()
        while t_secs > 0:
            mm, ss = divmod(t_secs, 60)
            t_display.markdown(f'<div class="timer-box">{mm:02d}:{ss:02d}</div>', unsafe_allow_html=True)
            time.sleep(1)
            t_secs -= 1
        st.balloons()

# --- MAIN INTERFACE ---
head_cols = st.columns([1, 5])
with head_cols[0]:
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=110)
with head_cols[1]:
    st.title("NotesAI: The Universal Learning Engine")
    st.write(f"🌐 Infrastructure Status: **Optimal** | 📅 {datetime.now().strftime('%A, %B %d, %Y')}")

st.markdown("""
<div class="feature-card">
    <h3>🌐 Multimodal Academic Intelligence</h3>
    NotesAI integrates vision-processing, linguistic synthesis, and adaptive testing. 
    <strong>Universal Syllabus Support Enabled.</strong>
</div>
""", unsafe_allow_html=True)

tips = [
    "🧠 **Memory Encoding:** Link new info to what you already know.",
    "🍅 **Neuro-Rest:** Take 5 min breaks every 25 mins.",
    "🔗 **Interleaving:** Mix subjects to improve problem-solving."
]
st.info(random.choice(tips))
st.divider()

# --- MODE LOGIC ---
if mode == "Tutor Chat":
    st.markdown("## 💬 AI Subject Specialist")
    subj = st.radio("Focus:", ["General", "Science", "History", "Math", "English", "Physics", "Chemistry"], horizontal=True)
    c_input = st.chat_input(f"Consult the {subj} Specialist...")
    if c_input:
        with st.spinner("Synthesizing..."):
            res = safe_ai_call(f"You are a {subj} tutor for an 8th grader. Explain: {c_input}")
            if res:
                st.chat_message("assistant", avatar="🎓").write(res)

elif mode == "Note Scanner":
    st.markdown("## 📸 Vision Analysis Core")
    up_file = st.file_uploader("📂 Input Notes", type=["jpg", "png", "jpeg"])
    if up_file:
        img = Image.open(up_file)
        c1, c2 = st.columns(2)
        with c1: st.image(img, use_container_width=True)
        with c2:
            s_type = st.select_slider("Depth", options=["Summary", "Transcription", "Concept Map"])
            if st.button("✨ START SCAN"):
                with st.spinner("Analyzing..."):
                    res = safe_ai_call([f"Perform a {s_type} on this image.", img])
                    if res:
                        st.write(res)
                        st.download_button("📥 Export", res, "NotesAI_Export.txt")

elif mode == "Exam Prep (Quiz)":
    st.markdown("## 📝 Assessment Engine")
    d_lvl = st.select_slider("Level:", options=["Elementary", "Intermediate", "Advanced", "Elite"], value="Intermediate")
    topic = st.text_input("Topic:", placeholder="e.g., Cellular Respiration")
    if st.button("🔥 GENERATE"):
        with st.spinner("Creating..."):
            res = safe_ai_call(f"Generate a 5-question {d_lvl} quiz on {topic}")
            if res:
                st.balloons()
                st.write(res)

st.divider()
st.caption("NotesAI Pro v4.2 | © 2026 STEM Excellence")
