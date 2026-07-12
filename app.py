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
    model = genai.GenerativeModel('gemini-2.5-flash') # Fallback clean default

# 2. UI Styling & Configuration
st.set_page_config(page_title="NotesAI v2.0", layout="wide", page_icon="🎓")

# Initialize Session States for Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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
        font-size: 36px;
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
    st.markdown("### 🎓 Academic Level")
    # UPGRADE: Added target curriculum selection for portfolio depth
    curriculum = st.selectbox("Target Curriculum", ["IGCSE", "IB Diploma Program", "IB MYP", "General High School"])
    
    st.markdown("### 📊 Learning Dashboard")
    target_mins = st.number_input("Target Study Minutes", min_value=1, max_value=480, value=60, step=15)
    completed_mins = st.slider("Minutes Completed", 0, target_mins, int(target_mins*0.65))
    
    progress_percentage = int((completed_mins / target_mins) * 100)
    st.progress(progress_percentage / 100)
    
    # FOCUS TIMER (Isolated in a fragment so it won't break the main screen UI)
    st.markdown("---")
    st.markdown("### ⏱️ Isolated Focus Timer")
    timer_minutes = st.number_input("Set Timer (mins)", min_value=1, max_value=120, value=25)
    
    @st.fragment
    def render_timer():
        if st.button("🚀 Start Timer", key="start_timer_btn"):
            t_seconds = timer_minutes * 60
            timer_display = st.empty()
            while t_seconds > 0:
                mins, secs = divmod(t_seconds, 60)
                timer_display.markdown(f'<div class="timer-box">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                time.sleep(1)
                t_seconds -= 1
            timer_display.success("⏰ Time's Up!")
            st.balloons()
            
    render_timer()
    st.caption(f"Status: Optimised for {curriculum} 🟢")

# --- MAIN CONTENT ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=100)
with col2:
    st.title("NotesAI v2.0")
    st.subheader("Your Intelligent Academic Study Partner")

st.markdown(f"""
<div class="feature-card">
    <strong>Welcome to version 2.0!</strong><br>
    Tailored to support your <strong>{curriculum}</strong> journey. 
    Decipher handwritten notes, converse with an AI Tutor, and track study milestones effortlessly.
</div>
""", unsafe_allow_html=True)

# --- MODE LOGIC ---
if mode == "Tutor Chat":
    st.markdown("### 💬 Interactive Tutor")
    subject = st.radio("Focus Area:", ["General", "Science", "History", "Math", "English"], horizontal=True)
    
    # Render historical messages from session state
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"], avatar="🎓" if message["role"] == "assistant" else None):
            st.write(message["content"])
            
    chat_input = st.chat_input("Type your question here...")
    
    if chat_input:
        # Display user message immediately
        st.chat_message("user").write(chat_input)
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        
        with st.spinner(f"NotesAI {subject} Specialist is thinking..."):
            try:
                # Upgraded prompt structure to include user chosen curriculum parameters
                prompt = (f"You are NotesAI, an expert tutor specializing in the {curriculum} framework. "
                          f"Explain the following concept perfectly tailored for a student studying {subject}: {chat_input}")
                
                response = model.generate_content(prompt)
                
                # Render and save assistant response
                with st.chat_message("assistant", avatar="🎓"):
                    st.write(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"AI Error: {e}")

elif mode == "Note Scanner":
    st.markdown("### 📸 Vision Scanner")
    st.write("Upload a photo of your notebook to create an AI-powered 'Cheat Sheet'.")
    
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        img_col, text_col = st.columns(2)
        with img_col:
            st.image(img, caption='Uploaded Notes', use_container_width=True)
        
        with text_col:
            if st.button("✨ Analyze & Summarize"):
                with st.spinner("Decoding handwriting and mapping concepts..."):
                    try:
                        prompt_msg = f"Provide a highly structured summary of these handwritten notes contextually fit for {curriculum} standards. Identify key definitions, terms, and core formulas."
                        response = model.generate_content([prompt_msg, img])
                        st.success("Analysis Complete!")
                        st.markdown("#### 📝 Notes Summary")
                        st.write(response.text)
                        st.download_button(label="📥 Download Study Summary", data=response.text, file_name="study_notes.txt", mime="text/plain")
                    except Exception as e:
                        st.error(f"AI Error: {e}")

elif mode == "Exam Prep (Quiz)":
    st.markdown("### 📝 Quiz Generator")
    diff = st.select_slider("Select Difficulty:", options=["Easy", "Medium", "Hard"], value="Medium")
    topic = st.text_input("What topic would you like to be tested on?", placeholder="e.g., Quadratic Equations, Cold War, Cell Mutation...")
    
    if st.button("🔥 Generate Practice Quiz"):
        with st.spinner(f"Generating a {diff} level quiz..."):
            try:
                prompt_msg = f"Generate a 5-question multiple choice quiz on the topic: '{topic}' matching the criteria of the {curriculum} curriculum at a {diff} level. Provide the answer key at the bottom."
                response = model.generate_content(prompt_msg)
                st.balloons() 
                st.markdown("---")
                st.markdown(f"### ❓ {curriculum} ({diff}) Practice Test: {topic}")
                st.write(response.text)
                st.download_button(label="📥 Download Quiz", data=response.text, file_name="quiz.txt", mime="text/plain")
            except Exception as e:
                st.error(f"AI Error: {e}")
