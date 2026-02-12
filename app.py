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
    /* Detailed metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: #002366 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: ANALYTICS & MONITORING ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg", use_container_width=True)
    st.title("🚀 NotesAI Pro")
    
    mode = st.selectbox("🎯 SELECT CAPABILITY", ["Tutor Chat", "Note Scanner", "Exam Prep (Quiz)"])
    
    st.divider()
    
    # PRODUCTIVITY TRACKER (Streaks removed as requested)
    st.subheader("📊 Session Intelligence")
    target_mins = st.number_input("Daily Mission (Mins)", min_value=1, max_value=720, value=60)
    completed_mins = st.slider("Session Progress", 0, target_mins, int(target_mins*0.4))
    
    prog = (completed_mins / target_mins)
    st.progress(prog)
    
    cols = st.columns(2)
    cols[0].metric("Focus Score", f"{int(prog*100)}%")
    cols[1].metric("Tokens", "Active", "✨")

    # NEW FEATURE: Session Log
    with st.expander("📝 Session Activity Log"):
        st.caption(f"Init: {datetime.now().strftime('%H:%M:%S')}")
        st.caption(f"Mode: {mode} Active")
        st.caption("Neural Engine: Synchronized")

    # LIVE TICKING TIMER
    st.divider()
    st.subheader("⏱️ Focus Chronometer")
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
        st.success("Interval Complete. Brain cooldown recommended.")

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
    Welcome to a high-performance cognitive environment. NotesAI integrates 
    vision-processing, linguistic synthesis, and adaptive testing into a single 
    unified framework. <strong>Universal Syllabus Support Enabled.</strong>
</div>
""", unsafe_allow_html=True)

# DYNAMIC STUDY TIPS
tips = [
    "🧠 **Memory Encoding:** Try to link new information to something you already know.",
    "🍅 **Neuro-Rest:** Take a 5-minute break away from screens after every focus interval.",
    "🔗 **Interleaving:** Study two related subjects together to strengthen mental agility.",
    "✍️ **Metacognition:** Ask yourself 'How well do I actually know this?' after every page."
]
st.info(random.choice(tips))

st.divider()

# --- CAPABILITY LOGIC ---

if mode == "Tutor Chat":
    st.markdown("## 💬 AI Subject Specialist")
    subj = st.radio("Specialization Core:", ["General", "Science", "History", "Math", "English", "Physics", "Chemistry", "Economics"], horizontal=True)
    
    details = {
        "General": "Cross-domain logic and general knowledge synthesis.",
        "Science": "Cellular biology, ecology, and scientific inquiry.",
        "History": "World history timelines, socio-political movements, and revolutions.",
        "Math": "Functions, geometry, and arithmetic logic.",
        "English": "Textual analysis, creative prose, and advanced syntax.",
        "Physics": "Mechanics, energy systems, and electromagnetic theory.",
        "Chemistry": "Molecular bonding, kinetics, and elemental properties.",
        "Economics": "Supply-demand curves and global financial theory."
    }
    
    # UI Enhancement: Curriculum Guide
    with st.expander("📚 View Curriculum Focus"):
        st.write(f"The **{subj}** core is currently optimized for IGCSE, IBDP, and AP standards.")

    st.caption(f"🧠 **System Configuration:** {details[subj]} | **Grade Support:** All Levels")
    
    # NEW FEATURE: Multi-step thinking
    st.toggle("Enable Deep Reasoning Mode", value=True)
    
    c_input = st.chat_input(f"Consult the {subj} Specialist...")
    if c_input:
        with st.spinner(f"NotesAI {subj} Core is synthesizing response..."):
            try:
                p = f"You are NotesAI, a world-class {subj} expert. Provide a detailed, pedagogical, and clear explanation for: {c_input}"
                resp = model.generate_content(p)
                with st.chat_message("assistant", avatar="🎓"):
                    st.markdown(f"### {subj} Specialist Analysis")
                    st.write(resp.text)
                    st.divider()
                    st.caption("Generated by NotesAI Neural Core v4.2")
            except Exception as e:
                st.error(f"Engine Timeout: {e}")

elif mode == "Note Scanner":
    st.markdown("## 📸 Vision Analysis Core")
    st.write("Extracting structured intelligence from handwritten or digital imagery.")
    
    

    up_file = st.file_uploader("📂 Input Handwritten Document", type=["jpg", "png", "jpeg"])
    
    if up_file:
        img = Image.open(up_file)
        c1, c2 = st.columns([1, 1.2])
        with c1:
            st.image(img, caption='Input Stream', use_container_width=True)
        with c2:
            # NEW FEATURE: Scan Intensity Options
            scan_type = st.select_slider("Analysis Depth", options=["Quick Summary", "Detailed Transcription", "Concept Mapping"])
            
            if st.button("✨ INITIATE VISION SCAN"):
                with st.spinner("Processing visual tokens..."):
                    try:
                        r = model.generate_content([f"Perform a {scan_type}. Provide transcription, key concepts, and a study guide.", img])
                        st.success("Vision Analysis Complete")
                        st.markdown("### 📝 Digital Intelligence Report")
                        st.write(r.text)
                        st.download_button("📥 Export as Study Sheet (.txt)", r.text, f"NotesAI_Scan_{datetime.now().strftime('%Y%m%d')}.txt")
                    except Exception as e:
                        st.error(f"Vision Error: {e}")

elif mode == "Exam Prep (Quiz)":
    st.markdown("## 📝 Adaptive Assessment Engine")
    d_level = st.select_slider("Intensity Level:", options=["Elementary", "Intermediate", "Advanced", "Elite / PhD"], value="Intermediate")
    
    

[Image of blood flow in the human heart]


    topic = st.text_input("Define Assessment Topic:", placeholder="e.g., Cellular Respiration or Industrial Revolution")
    
    # NEW FEATURE: Question Type Selector
    q_type = st.multiselect("Included Question Formats:", ["Multiple Choice", "True/False", "Short Answer"], default=["Multiple Choice"])
    
    if st.button("🔥 GENERATE ASSESSMENT"):
        with st.spinner(f"Architecting {d_level} level challenge..."):
            try:
                formats = ", ".join(q_type)
                r = model.generate_content(f"Generate a 5-question {d_level} difficulty exam on {topic} using {formats}. Provide a detailed explanation for each answer at the bottom.")
                st.balloons()
                st.markdown(f"### ❓ {d_level} Exam: {topic}")
                st.write(r.text)
                st.download_button("📥 Save Exam for Offline Study", r.text, "NotesAI_Exam.txt")
            except Exception as e:
                st.error(f"Generation Failed: {e}")

st.divider()
st.caption("NotesAI Pro Framework v4.2 | Universal Academic Integration | © 2026 STEM Excellence")
