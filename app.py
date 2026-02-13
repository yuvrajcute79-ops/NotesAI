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
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception:
    model = genai.GenerativeModel('gemini-1.5-flash')

# 2. UI Styling & Configuration
st.set_page_config(page_title="NotesAI Pro", layout="wide", page_icon="🎓")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

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

# --- SIDEBAR GRAPHICS & TIMER ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg", use_container_width=True)
    st.header("📌 Navigation")
    mode = st.selectbox("Choose a Study Mode", ["Tutor Chat", "Note Scanner", "Exam Prep (Quiz)"])
    
    # NEW FEATURE: Language Support
    st.divider()
    language = st.selectbox("🌍 Learning Language", ["English", "Spanish", "French", "German", "Hindi"])

    st.markdown("---")
    st.markdown("### 📊 Learning Dashboard")
    st.metric(label="System Status", value="Active", delta="100% Uptime")
    
    st.markdown("---")
    st.markdown("### 📈 Goal Customization")
    target_mins = st.number_input("Target Study Minutes", min_value=1, max_value=480, value=60, step=15)
    completed_mins = st.slider("Minutes Completed", 0, target_mins, int(target_mins*0.65))
    
    progress_percentage = int((completed_mins / target_mins) * 100)
    st.progress(progress_percentage / 100)
    
    if progress_percentage < 40:
        st.warning(f"Level: Beginner ({progress_percentage}%)")
    elif progress_percentage < 80:
        st.info(f"Level: Intermediate ({progress_percentage}%)")
    else:
        st.success(f"Level: Master Scholar ({progress_percentage}%)")

    # FOCUS TIMER
    st.markdown("---")
    st.markdown("### ⏱️ Live Focus Timer")
    timer_minutes = st.number_input("Set Timer (mins)", min_value=1, max_value=120, value=25)
    
    if st.button("🚀 Start Timer"):
        t_seconds = timer_minutes * 60
        timer_display = st.empty()
        while t_seconds > 0:
            mins, secs = divmod(t_seconds, 60)
            timer_display.markdown(f'<div class="timer-box">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
            time.sleep(1)
            t_seconds -= 1
        timer_display.success("⏰ Time's Up! Take a break.")
        st.balloons()
    
    st.caption(f"Status: Ready for IGCSE/IB Support 🟢 ({language})")

# --- MAIN CONTENT ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=100)
with col2:
    st.title("NotesAI Pro")
    st.subheader("Your Intelligent Academic Study Partner")

st.markdown("""
<div class="feature-card">
    <strong>Welcome to the Pro Edition!</strong><br>
    Bridging the gap between handwritten notes and digital mastery. Now supporting multi-language explanations and persistent chat history.
</div>
""", unsafe_allow_html=True)

tips = [
    "Use active recall: Test yourself instead of just re-reading.",
    "Space out your study sessions for better long-term memory.",
    "Try explaining a topic to an imaginary student to find your knowledge gaps.",
    "Take 5-minute breaks every 25 minutes (Pomodoro technique)."
]
st.info(f"💡 **Study Tip:** {random.choice(tips)}")

st.divider()

# --- MODE LOGIC ---
if mode == "Tutor Chat":
    st.markdown("### 💬 Interactive Tutor")
    subject = st.radio("Focus Area:", ["General", "Science", "History", "Math", "English"], horizontal=True)
    
    # NEW FEATURE: Display History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat_input = st.chat_input("Ask a question...")
    if chat_input:
        st.session_state.messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)

        with st.spinner(f"NotesAI {subject} Specialist is thinking in {language}..."):
            try:
                prompt = f"Role: Specialist {subject} tutor for 8th grade. Language: {language}. Task: Explain {chat_input}"
                response = model.generate_content(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant", avatar="🎓"):
                    st.write(response.text)
            except Exception as e:
                st.error(f"AI Error: {e}")

elif mode == "Note Scanner":
    st.markdown("### 📸 Vision Scanner")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        img_col, text_col = st.columns(2)
        with img_col:
            st.image(img, caption='Uploaded Notes', use_container_width=True)
        
        with text_col:
            analysis_type = st.radio("Scanner Mode", ["Standard Summary", "Extract Formulas", "Key Dates & Names"])
            if st.button("✨ Analyze & Summarize"):
                with st.spinner("Decoding notes..."):
                    try:
                        # NEW FEATURE: Targeted Extraction
                        prompt = f"In {language}, provide a structured {analysis_type} of these notes. Extract specific {analysis_type} if visible."
                        response = model.generate_content([prompt, img])
                        st.success("Extraction Complete!")
                        st.write(response.text)
                        st.download_button(label="📥 Download Study Summary", data=response.text, file_name="study_notes.txt")
                    except Exception as e:
                        st.error(f"AI Error: {e}")

elif mode == "Exam Prep (Quiz)":
    st.markdown("### 📝 Quiz Generator")
    diff = st.select_slider("Select Difficulty:", options=["Easy", "Medium", "Hard"], value="Medium")
    topic = st.text_input("Topic for test:")
    
    if st.button("🔥 Generate Practice Quiz"):
        with st.spinner(f"Architecting {diff} test..."):
            try:
                # NEW FEATURE: Structured Quiz Formatting
                prompt = f"Create a 5-question {diff} quiz in {language} about {topic} for 8th grade. Use MCQ format. Hide the answers at the very bottom."
                response = model.generate_content(prompt)
                st.session_state.last_quiz = response.text
                st.balloons() 
                st.markdown(f"### ❓ {diff} Quiz: {topic}")
                st.write(st.session_state.last_quiz)
                st.download_button(label="📥 Download Quiz", data=st.session_state.last_quiz, file_name="quiz.txt")
            except Exception as e:
                st.error(f"AI Error: {e}")
