import streamlit as st
import google.generativeai as genai
from PIL import Image
import random 
import time   

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
st.set_page_config(page_title="NotesAI", layout="wide", page_icon="🎓")

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
        border: none;
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
    .stProgress > div > div > div > div {
        background-color: #002366;
    }
    .timer-box {
        font-size: 50px;
        font-weight: bold;
        color: #002366;
        text-align: center;
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        border: 2px solid #002366;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR GRAPHICS & ENHANCED DASHBOARD ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg", use_container_width=True)
    st.header("📌 Navigation")
    mode = st.selectbox("Choose a Study Mode", ["Tutor Chat", "Note Scanner", "Exam Prep (Quiz)"])
    
    st.divider()
    st.markdown("### 📊 Learning Dashboard")
    st.metric(label="System Status", value="Active", delta="⚡ Optimized")
    
    st.markdown("---")
    st.markdown("### 📈 Goal Customization")
    target_mins = st.number_input("Daily Target (Mins)", min_value=1, max_value=480, value=60, step=15)
    completed_mins = st.slider("Current Progress", 0, target_mins, int(target_mins*0.65))
    
    progress_percentage = int((completed_mins / target_mins) * 100)
    st.progress(progress_percentage / 100)
    
    # Progress Level Graphics
    if progress_percentage < 40:
        st.warning(f"Level: Novice Explorer 🥉 ({progress_percentage}%)")
    elif progress_percentage < 80:
        st.info(f"Level: Knowledge Seeker 🥈 ({progress_percentage}%)")
    else:
        st.success(f"Level: Master Scholar 🥇 ({progress_percentage}%)")

    # FOCUS TIMER (ACTUAL TICKING TIMER)
    st.markdown("---")
    st.markdown("### ⏱️ Live Focus Timer")
    timer_minutes = st.number_input("Set Session (mins)", min_value=1, max_value=120, value=25)
    
    if st.button("🚀 Start Study Session"):
        t_seconds = timer_minutes * 60
        timer_display = st.empty()
        while t_seconds > 0:
            mins, secs = divmod(t_seconds, 60)
            timer_display.markdown(f'<div class="timer-box">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
            time.sleep(1)
            t_seconds -= 1
        timer_display.success("⏰ Session Complete! Your brain deserves a break.")
        st.balloons()
    
    st.caption("Status: Ready for IGCSE/IB Support 🟢")

# --- MAIN CONTENT GRAPHICS ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=100)
with col2:
    st.title("NotesAI")
    st.subheader("Your Intelligent Academic Study Partner")

st.markdown("""
<div class="feature-card">
    <strong>Welcome to the future of studying!</strong><br>
    It is designed specifically for <strong>Students</strong> to bridge the gap between handwritten notes and digital mastery. 
    Our AI engine can decipher complex handwriting, simplify concepts and verify your knowledge through our quiz feature.
</div>
""", unsafe_allow_html=True)

# STUDY TIP
tips = [
    "Use active recall: Test yourself instead of just re-reading.",
    "Space out your study sessions for better long-term memory.",
    "Try explaining a topic to an imaginary student to find your knowledge gaps.",
    "Take 5-minute breaks every 25 minutes (Pomodoro technique)."
]
st.info(f"💡 **Study Tip of the Day:** {random.choice(tips)}")

st.divider()

# --- MODE LOGIC ---
if mode == "Tutor Chat":
    st.markdown("### 💬 Interactive Tutor")
    subject = st.radio("Focus Area:", ["General", "Science", "History", "Math", "English"], horizontal=True)
    
    # Enhanced Subject Specific Details
    details = {
        "General": "Comprehensive support for various subjects and curricula.",
        "Science": "Focus on Physics, Chemistry, and Biology laws, collision theory, and atomic structures.",
        "History": "Timeline analysis, the Revolt of 1857, and the Indian National Movement.",
        "Math": "Algebraic identities, geometry proofs, and arithmetic progression.",
        "English": "Literary devices, essay structures, grammar, and poetry analysis."
    }
    
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.caption(f"🎯 **Specialization:** {details[subject]}")
        st.write(f"Ask any **{subject}** question below for a detailed academic explanation.")
    with col_right:
        # Mini Subject Card
        st.markdown(f"""
        <div style="padding:10px; border-radius:10px; background-color:#e0eafc; border-left:5px solid #002366;">
        <strong>Mode:</strong> {subject} Specialist<br>
        <strong>Grade:</strong> 8-12 Support
        </div>""", unsafe_allow_html=True)
    
    chat_input = st.chat_input("Type your question here...")
    if chat_input:
        with st.spinner(f"NotesAI {subject} Specialist is drafting a response..."):
            try:
                prompt = f"You are NotesAI, a specialist {subject} tutor for an 8th grader. Explain this clearly: {chat_input}"
                response = model.generate_content(prompt)
                st.chat_message("assistant", avatar="🎓").write(response.text)
            except Exception as e:
                st.error(f"AI Error: {e}")

elif mode == "Note Scanner":
    st.markdown("### 📸 Vision Scanner")
    st.write("Upload a photo of your notebook to create a summarized 'Cheat Sheet'.")
    
    
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        img_col, text_col = st.columns(2)
        with img_col:
            st.image(img, caption='Uploaded Notes', use_container_width=True)
        
        with text_col:
            if st.button("✨ Analyze & Summarize"):
                with st.spinner("Deciphering handwriting and extracting key concepts..."):
                    try:
                        response = model.generate_content(["Provide a structured summary of these notes with key terms, definitions, and a list of formulas if present.", img])
                        st.success("Data Extraction Complete!")
                        st.markdown("#### 📝 Notes Summary")
                        st.write(response.text)
                        st.download_button(label="📥 Download Study Summary", data=response.text, file_name="study_notes.txt", mime="text/plain")
                    except Exception as e:
                        st.error(f"AI Error: {e}")

elif mode == "Exam Prep (Quiz)":
    st.markdown("### 📝 Quiz Generator")
    diff = st.select_slider("Select Difficulty:", options=["Easy", "Medium", "Hard", "Master"], value="Medium")
    
    topic = st.text_input("What topic would you like to be tested on?", placeholder="Enter topic here...")
    
    if st.button("🔥 Generate Practice Quiz"):
        with st.spinner(f"Generating {diff} difficulty test..."):
            try:
                response = model.generate_content(f"Generate a 5-question {diff} level multiple choice quiz on {topic} for an 8th-grade student. Include answers at the end.")
                st.balloons() 
                st.markdown("---")
                st.markdown(f"### ❓ {diff} Practice Quiz: {topic}")
                st.write(response.text)
                st.download_button(label="📥 Download Quiz for Later", data=response.text, file_name="quiz.txt", mime="text/plain")
            except Exception as e:
                st.error(f"AI Error: {e}")
