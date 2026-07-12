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

# --- 2. PAGE STYLING & INITIALIZATION ---
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

# Custom CSS for Glassmorphism, Gradients, and the Easter Egg
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    
    /* Title Gradient */
    .title-glow {
        background: -webkit-linear-gradient(45deg, #002366, #6b00b3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: 900;
    }
    
    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.3);
        margin-bottom: 20px;
    }
    
    /* Timer Box */
    .timer-box {
        font-size: 36px;
        font-weight: bold;
        color: #002366;
        text-align: center;
        background: #e0eafc;
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Secret Developer Text (Matches background color) */
    .easter-egg {
        color: #f4f6f9; 
        text-align: center;
        font-size: 12px;
        margin-top: 50px;
        user-select: all;
    }
    .easter-egg:hover {
        color: #d1d5db; /* Slightly reveals on hover */
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (DASHBOARD & TIMER) ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg", use_container_width=True)
    
    st.markdown("### 🏆 Student Profile")
    st.metric(label="Total Knowledge XP", value=f"{st.session_state.xp_points} XP")
    
    if st.session_state.xp_points < 50:
        st.caption("Current Rank: Novice Explorer 🥉")
    elif st.session_state.xp_points < 150:
        st.caption("Current Rank: Dedicated Scholar 🥈")
    else:
        st.caption("Current Rank: Academic Mastermind 🥇")

    st.markdown("---")
    st.markdown("### 🎧 Focus Radio (Lo-Fi)")
    # YouTube Iframe for Lofi Girl 24/7 Stream
    components.iframe("https://www.youtube.com/embed/jfKfPfyJRdk", height=200)

    st.markdown("---")
    st.markdown("### ⏱️ Focus Timer")
    timer_minutes = st.number_input("Set Timer (mins)", min_value=1, max_value=120, value=25)
    
    @st.fragment
    def render_timer():
        btn_ph = st.empty()
        timer_ph = st.empty()

        if not st.session_state.timer_running:
            if btn_ph.button("🚀 Start Timer", key="start_btn", use_container_width=True):
                st.session_state.timer_running = True
                st.session_state.timer_seconds = timer_minutes * 60
                st.rerun()
        else:
            if btn_ph.button("🛑 Stop Timer", key="stop_btn", use_container_width=True):
                st.session_state.timer_running = False
                st.session_state.timer_seconds = 0
                timer_ph.empty()
                st.rerun()

            while st.session_state.timer_seconds > 0 and st.session_state.timer_running:
                mins, secs = divmod(st.session_state.timer_seconds, 60)
                timer_ph.markdown(f'<div class="timer-box">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                time.sleep(1)
                st.session_state.timer_seconds -= 1
            
            if st.session_state.timer_running:
                st.session_state.timer_running = False
                timer_ph.success("⏰ Time's Up!")
                st.balloons()
                st.session_state.xp_points += 10 # Reward for finishing timer!
                st.toast("🎉 +10 XP for completing a Focus Session!")
                time.sleep(2)
                st.rerun()
                
    render_timer()

# --- 4. MAIN SCREEN (TABS) ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=80)
with col2:
    st.markdown('<div class="title-glow">NotesAI</div>', unsafe_allow_html=True)
    st.markdown("**Your Intelligent Academic Study Partner**")

st.markdown("""
<div class="glass-card">
    Welcome back! NotesAI is optimized to help you master your <strong>IGCSE framework</strong> and 9th-grade curriculum. 
    Choose a tool below to begin earning XP.
</div>
""", unsafe_allow_html=True)

# Create 3 Modern Tabs
tab1, tab2, tab3 = st.tabs(["💬 Interactive Tutor", "📸 Vision Scanner", "📝 Quiz Generator"])

# --- TAB 1: INTERACTIVE TUTOR ---
with tab1:
    st.markdown("### 💬 Your Personal IGCSE Tutor")
    
    # Clear Chat Button
    col_chat1, col_chat2 = st.columns([4, 1])
    with col_chat2:
        if st.button("✨ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # Display History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"], avatar="🎓" if message["role"] == "assistant" else None):
            st.write(message["content"])
            
    chat_input = st.chat_input("Ask a question (e.g., 'Explain the carbon cycle')...")
    
    if chat_input:
        st.chat_message("user").write(chat_input)
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        
        with st.spinner("NotesAI is thinking..."):
            try:
                # Hardcoded IGCSE Persona
                prompt = (f"You are NotesAI, an expert, friendly tutor specializing in the IGCSE framework for a 9th-grade student. "
                          f"Provide a clear, engaging, and highly accurate response to this: {chat_input}")
                response = model.generate_content(prompt)
                
                with st.chat_message("assistant", avatar="🎓"):
                    st.write(response.text)
                
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                
                # Gamification
                st.session_state.xp_points += 5
                st.toast("🎉 +5 XP for asking a great question!")
            except Exception as e:
                st.error(f"AI Error: {e}")

# --- TAB 2: VISION SCANNER ---
with tab2:
    st.markdown("### 📸 Turn Handwriting into Cheat Sheets")
    uploaded_file = st.file_uploader("Upload Notebook Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Notes', use_container_width=True)
        
        if st.button("✨ Analyze & Summarize Notes", use_container_width=True):
            with st.spinner("Decoding handwriting and mapping concepts..."):
                try:
                    prompt_msg = "Provide a structured summary of these handwritten notes fit for the IGCSE standard. Identify key definitions, terms, and core formulas."
                    response = model.generate_content([prompt_msg, img])
                    
                    st.success("Analysis Complete!")
                    st.markdown("#### 📝 Notes Summary")
                    st.write(response.text)
                    
                    # Add Custom Watermark
                    watermarked_text = response.text + "\n\n---\nMade by NotesAI™"
                    st.download_button(label="📥 Download Study Summary", data=watermarked_text, file_name="NotesAI_Summary.txt", mime="text/plain", use_container_width=True)
                    
                    st.session_state.xp_points += 20
                    st.toast("🎉 +20 XP: Notes Transformed!")
                except Exception as e:
                    st.error(f"AI Error: {e}")

# --- TAB 3: QUIZ GENERATOR ---
with tab3:
    st.markdown("### 📝 Instant IGCSE Practice Tests")
    topic = st.text_input("Topic to test on:", placeholder="e.g., Quadratic Equations, World War I, Cell Structure...")
    diff = st.select_slider("Select Difficulty:", options=["Easy", "Medium", "Hard"], value="Medium")
    
    if st.button("🔥 Generate Practice Quiz", use_container_width=True):
        if topic:
            with st.spinner(f"Generating a {diff} level quiz..."):
                try:
                    prompt_msg = f"Generate a 5-question multiple choice quiz on the topic: '{topic}'. Tailor it to the IGCSE curriculum at a {diff} difficulty level for a 9th grader. Provide the answer key at the very bottom."
                    response = model.generate_content(prompt_msg)
                    
                    st.balloons() 
                    st.markdown(f"### ❓ Practice Test: {topic}")
                    st.write(response.text)
                    
                    # Add Custom Watermark
                    watermarked_quiz = response.text + "\n\n---\nMade by NotesAI™"
                    st.download_button(label="📥 Download Quiz", data=watermarked_quiz, file_name=f"NotesAI_Quiz_{topic}.txt", mime="text/plain", use_container_width=True)
                    
                    st.session_state.xp_points += 15
                    st.toast("🎉 +15 XP: Quiz Generated!")
                except Exception as e:
                    st.error(f"AI Error: {e}")
        else:
            st.warning("Please enter a topic first!")

# --- 5. THE EASTER EGG ---
# This text blends into the background color and is only visible if highlighted!
st.markdown('<div class="easter-egg">made by Yuvraj jain</div>', unsafe_allow_html=True)
