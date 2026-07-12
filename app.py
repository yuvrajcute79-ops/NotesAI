import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import time

# --- 1. API CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets!")

try:
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. PAGE INITIALIZATION ---
st.set_page_config(page_title="NotesAI", layout="wide", page_icon="🎓")

# Initialize Session States (Memory)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "xp_points" not in st.session_state:
    st.session_state.xp_points = 0
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 0

# Light custom styling just to ensure timer text stays uniform
st.markdown("""
    <style>
    .timer-display {
        font-size: 42px;
        font-weight: bold;
        color: #ffcc00;
        text-align: center;
        background: #1e293b;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #334155;
    }
    .easter-egg {
        color: transparent; 
        text-align: center;
        font-size: 11px;
        margin-top: 60px;
        user-select: all;
    }
    .easter-egg:hover {
        color: #475569;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg", use_container_width=True)
    
    st.markdown("## 🏆 Academic Profile")
    st.metric(label="Total Knowledge XP", value=f"{st.session_state.xp_points} XP")
    
    if st.session_state.xp_points < 50:
        st.info("Rank: Novice Explorer 🥉")
    elif st.session_state.xp_points < 150:
        st.success("Rank: Dedicated Scholar 🥈")
    else:
        st.warning("Rank: Academic Mastermind 🥇")

    st.markdown("---")
    st.markdown("### 🎧 Focus Radio (Lo-Fi)")
    # Upgraded embed with explicit control tags allowing player interaction
    components.iframe("https://www.youtube.com/embed/jfKfPfyJRdk?controls=1&rel=0", height=180)
    st.caption("💡 Remember to click play inside the box to start audio!")

    st.markdown("---")
    st.markdown("### ⏱️ Focus Timer")
    timer_minutes = st.number_input("Set Timer (mins)", min_value=1, max_value=120, value=25)
    
    @st.fragment
    def render_timer():
        btn_ph = st.empty()
        timer_ph = st.empty()

        if not st.session_state.timer_running:
            if btn_ph.button("🚀 Start Focus", key="start_btn", use_container_width=True):
                st.session_state.timer_running = True
                st.session_state.timer_seconds = timer_minutes * 60
                st.rerun()
        else:
            if btn_ph.button("🛑 Stop Focus", key="stop_btn", use_container_width=True):
                st.session_state.timer_running = False
                st.session_state.timer_seconds = 0
                timer_ph.empty()
                st.rerun()

            while st.session_state.timer_seconds > 0 and st.session_state.timer_running:
                mins, secs = divmod(st.session_state.timer_seconds, 60)
                timer_ph.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                time.sleep(1)
                st.session_state.timer_seconds -= 1
            
            if st.session_state.timer_running:
                st.session_state.timer_running = False
                timer_ph.success("⏰ Time's Up! Focus completed.")
                st.balloons()
                st.session_state.xp_points += 10
                st.toast("🎉 +10 XP for completing a Focus Session!")
                time.sleep(2)
                st.rerun()
                
    render_timer()
    st.caption("Curriculum Context: IGCSE Target 🟢")

# --- 4. MAIN CONTENT AREA ---
header_col1, header_col2 = st.columns([1, 6])
with header_col1:
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=75)
with header_col2:
    st.title("NotesAI v2.0")
    st.write("*Your Intelligent Academic Study Partner for IGCSE Mastery*")

# High-contrast, completely native informational callout box
st.info(
    "👋 **Welcome to NotesAI v2.0!** Highly optimized to assist with the 9th-grade IGCSE framework. "
    "Select one of our core modular tabs below to start organizing notes, quizzing yourself, or consulting the interactive tutor."
)

st.divider()

# Core Navigation Tabs
tab1, tab2, tab3 = st.tabs(["💬 Interactive Tutor", "📸 Vision Note Scanner", "📝 Exam Prep Quizzer"])

# --- TAB 1: INTERACTIVE TUTOR ---
with tab1:
    st.markdown("### 💬 Real-Time IGCSE Tutor Chat")
    
    subject = st.radio("Focus Area:", ["General", "Science", "History", "Math", "English"], horizontal=True)
    
    # Render historical messages from session state
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"], avatar="🎓" if message["role"] == "assistant" else None):
            st.write(message["content"])
            
    chat_input = st.st.chat_input("Ask a question about your topics...")
    
    # Catching edge case where chat_input wasn't rendering cleanly
    if chat_input:
        st.chat_message("user").write(chat_input)
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        
        # Simple, high-compatibility spinner text instead of customized blocks
        with st.status("NotesAI is processing concept query..."):
            try:
                prompt = (f"You are NotesAI, a helpful tutor specializing in the IGCSE system. "
                          f"Explain this concept cleanly for a 9th-grade student concentrating on {subject}: {chat_input}")
                response = model.generate_content(prompt)
                
                with st.chat_message("assistant", avatar="🎓"):
                    st.write(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                
                st.session_state.xp_points += 5
                st.toast("🎉 +5 XP for engaging with the tutor!")
            except Exception as e:
                st.error(f"AI System Error: {e}")

    if st.session_state.chat_history:
        st.write("")
        if st.button("✨ Reset Conversation Loop", key="clear_chat_button"):
            st.session_state.chat_history = []
            st.rerun()

# --- TAB 2: NOTE SCANNER ---
with tab2:
    st.markdown("### 📸 Vision Optical Handwriting Decoder")
    st.write("Upload an image of your notebook pages to generate an structured summary sheet.")
    
    uploaded_file = st.file_uploader("Upload Image File", type=["jpg", "png", "jpeg"], key="scanner_upload")
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Document Context', use_container_width=True)
        
        if st.button("✨ Execute AI Concept Mapping", use_container_width=True):
            with st.status("Extracting and mapping definitions..."):
                try:
                    prompt_msg = "Extract all clear handwritten text from this note picture and rewrite it as an organized study summary fit for IGCSE parameters."
                    response = model.generate_content([prompt_msg, img])
                    
                    st.success("Analysis Complete!")
                    st.write(response.text)
                    
                    final_download = response.text + "\n\n---\nMade by NotesAI™"
                    st.download_button(label="📥 Download Study Summary", data=final_download, file_name="NotesAI_CheatSheet.txt", mime="text/plain", use_container_width=True)
                    
                    st.session_state.xp_points += 20
                    st.toast("🎉 +20 XP: Handwritten data structured successfully!")
                except Exception as e:
                    st.error(f"Vision Processing Error: {e}")

# --- TAB 3: QUIZ GENERATOR ---
with tab3:
    st.markdown("### 📝 IGCSE Target Quiz Generator")
    topic = st.text_input("Enter evaluation topic:", placeholder="e.g., Photosynthesis, Cell Division, Linear Equations...", key="quiz_topic")
    diff = st.select_slider("Select Academic Rigour Level:", options=["Easy", "Medium", "Hard"], value="Medium")
    
    if st.button("🔥 Generate Practice Assessment", use_container_width=True):
        if topic:
            with st.status(f"Structuring {diff}-level exam questions..."):
                try:
                    prompt_msg = f"Draft a 5-question multiple choice test focused specifically on '{topic}' aligning with the standard expectations of IGCSE criteria at a {diff} level. Show answers at the very end."
                    response = model.generate_content(prompt_msg)
                    
                    st.balloons()
                    st.markdown("---")
                    st.write(response.text)
                    
                    final_quiz = response.text + "\n\n---\nMade by NotesAI™"
                    st.download_button(label="📥 Save Examination Sheet", data=final_quiz, file_name=f"NotesAI_Quiz_{topic}.txt", mime="text/plain", use_container_width=True)
                    
                    st.session_state.xp_points += 15
                    st.toast("🎉 +15 XP: Practice quiz added to profile tracking!")
                except Exception as e:
                    st.error(f"Quiz Generation Error: {e}")
        else:
            st.warning("Please type a topic target field before executing execution loops.")

# --- 5. THE SECRET TEXT ---
st.markdown('<div class="easter-egg">made by Yuvraj jain</div>', unsafe_allow_html=True)
