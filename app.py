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

# --- 2. DEEP THINKING & CACHING LOGIC (The "No-Repeat" Fix) ---
@st.cache_data(ttl=600, show_spinner=False)
def get_ai_response(prompt_data, is_image=False):
    """Saves AI answers for 10 mins to avoid hitting quota twice."""
    try:
        response = model.generate_content(prompt_data)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "THINKING_REQUIRED"
        return f"Error: {e}"

def handle_deep_thinking():
    """Triggered when Quota is hit: Shows facts + progress bar."""
    study_facts = [
        "🧠 Your brain uses 20% of your body's total energy!",
        "⚡ Neurons in your brain travel at 270 km/h.",
        "📖 Reading for 6 mins reduces stress by 68%.",
        "🍌 Bananas are berries, but strawberries aren't!",
        "🦈 Sharks have existed for longer than trees.",
        "🪐 A day on Venus is longer than a year on Venus."
    ]
    st.info("🧠 **NotesAI is Thinking Deeply...**")
    st.markdown(f"***Did you know?*** *{random.choice(study_facts)}*")
    
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.6) # 60s cooldown
        progress_bar.progress(percent_complete + 1)
    st.success("✨ Deep thought complete! Please try your request again.")

# --- 3. ACCOUNT SYSTEM GATEWAY ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_db' not in st.session_state:
    st.session_state.user_db = {"admin": "password123"}

def login_page():
    st.markdown("<h1 style='text-align: center; color: #002366;'>🎓 NotesAI Pro</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Enter Dashboard"):
            if u in st.session_state.user_db and st.session_state.user_db[u] == p:
                st.session_state.authenticated = True
                st.session_state.current_user = u
                st.rerun()
            else: st.error("Wrong details.")
    with tab2:
        new_u = st.text_input("New Username")
        new_p = st.text_input("New Password", type="password")
        if st.button("Create Profile"):
            st.session_state.user_db[new_u] = new_p
            st.success("Profile Created!")

if not st.session_state.authenticated:
    login_page()
    st.stop()

# --- 4. MAIN APP INTERFACE ---
st.set_page_config(page_title="NotesAI Pro", layout="wide", page_icon="🎓")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div.stButton > button:first-child {
        background-color: #002366; color: white; border-radius: 12px; font-weight: bold;
    }
    .feature-card {
        background: white; padding: 25px; border-radius: 15px; border-left: 5px solid #002366;
    }
    .timer-box {
        font-size: 50px; font-weight: bold; color: #002366; text-align: center;
        background: #eef2f3; border-radius: 20px; padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg")
    st.title("🚀 NotesAI Pro")
    st.write(f"👤 Scholar: **{st.session_state.current_user}**")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
    
    mode = st.selectbox("🎯 CAPABILITY", ["Tutor Chat", "Note Scanner", "Exam Prep"])
    st.divider()
    t_mins = st.number_input("Study Time (Mins)", 1, 120, 25)
    if st.button("⏱️ START TIMER"):
        ts = t_mins * 60
        td = st.empty()
        while ts > 0:
            mm, ss = divmod(ts, 60)
            td.markdown(f'<div class="timer-box">{mm:02d}:{ss:02d}</div>', unsafe_allow_html=True)
            time.sleep(1); ts -= 1
        st.balloons()

# --- 5. LOGIC MODULES ---
st.title("NotesAI: The Specialized Learning Engine")

if mode == "Tutor Chat":
    subj = st.radio("Subject:", ["Science", "History", "Math", "English", "Economics"], horizontal=True)
    prompt = st.chat_input("Ask your question...")
    if prompt:
        with st.spinner("AI is thinking..."):
            ans = get_ai_response(f"As a {subj} tutor, explain: {prompt}")
            if ans == "THINKING_REQUIRED": handle_deep_thinking()
            else: st.chat_message("assistant", avatar="🎓").write(ans)

elif mode == "Note Scanner":
    f = st.file_uploader("Upload Notes", type=["jpg","png","jpeg"])
    if f:
        img = Image.open(f)
        st.image(img, width=400)
        if st.button("✨ SCAN NOTES"):
            with st.spinner("Processing..."):
                # Note: Images aren't cached the same way as text strings
                try:
                    res = model.generate_content(["Summarize these handwritten notes.", img])
                    st.write(res.text)
                except Exception as e:
                    if "429" in str(e): handle_deep_thinking()

elif mode == "Exam Prep":
    topic = st.text_input("Quiz Topic:")
    if st.button("🔥 GENERATE QUIZ"):
        with st.spinner("Creating..."):
            ans = get_ai_response(f"Create a 5-question quiz on {topic}")
            if ans == "THINKING_REQUIRED": handle_deep_thinking()
            else: st.write(ans)

st.divider()
st.caption("NotesAI Pro v5.2 | Final Market Prototype | © 2026 STEM Excellence")
