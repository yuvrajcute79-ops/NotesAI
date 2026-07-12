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

# --- 2. PAGE INITIALIZATION & CLAUDE-STYLE CSS ---
st.set_page_config(page_title="NotesAI", layout="wide", page_icon="✦")

# Initialize Session States (Memory)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "xp_points" not in st.session_state:
    st.session_state.xp_points = 0
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 0

# Ultra-clean, minimalist CSS inspired by Anthropic
st.markdown("""
    <style>
    .main { background-color: #fdfdfc; color: #1a1a1a; font-family: 'Inter', sans-serif; }
    
    h1, h2, h3 { color: #2d2d2d; font-weight: 600; }
    
    .timer-display {
        font-size: 38px;
        font-weight: 400;
        color: #1a1a1a;
        text-align: center;
        background: #f3f3f2;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #e5e5e5;
        font-family: monospace;
    }
    
    /* Clean Divider */
    hr { border-top: 1px solid #e5e5e5; }
    
    /* Secret Developer Text */
    .easter-egg {
        color: transparent; 
        text-align: center;
        font-size: 11px;
        margin-top: 80px;
        user-select: all;
    }
    .easter-egg:hover { color: #d4d4d4; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (MINIMALIST DASHBOARD) ---
with st.sidebar:
    st.markdown("### ✦ NotesAI Workspace")
    st.caption("Curriculum Context: 9th-Grade IGCSE")
    st.markdown("---")
    
    st.markdown("#### Activity Metrics")
    st.metric(label="Knowledge XP", value=f"{st.session_state.xp_points}")
    
    progress = min(st.session_state.xp_points / 100.0, 1.0)
    st.progress(progress, text="Daily Target (100 XP)")
    
    st.markdown("---")
    st.markdown("#### Focus Environment")
    components.iframe("https://www.youtube.com/embed/jfKfPfyJRdk?controls=1&rel=0", height=180)
    
    st.markdown("---")
    timer_minutes = st.number_input("Session Length (mins)", min_value=1, max_value=120, value=25)
    
    @st.fragment
    def render_timer():
        btn_ph = st.empty()
        timer_ph = st.empty()

        if not st.session_state.timer_running:
            if btn_ph.button("Start Focus Session", key="start_btn", use_container_width=True):
                st.session_state.timer_running = True
                st.session_state.timer_seconds = timer_minutes * 60
                st.rerun()
        else:
            if btn_ph.button("End Session", key="stop_btn", use_container_width=True):
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
                timer_ph.success("Focus complete.")
                st.session_state.xp_points += 20
                st.toast("✦ 20 XP Earned")
                time.sleep(2)
                st.rerun()
                
    render_timer()

# --- 4. MAIN CONTENT AREA ---
st.title("NotesAI")
st.write("An intelligent, highly structured academic environment tailored for your IGCSE framework.")
st.divider()

# Core Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Chat", "Vision", "Assess", "Flashcards", "Review"])

# --- TAB 1: INTERACTIVE TUTOR ---
with tab1:
    subject = st.radio("Context:", ["General", "Science", "History", "Math", "English"], horizontal=True)
    st.markdown("---")
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"], avatar="✦" if message["role"] == "assistant" else "👤"):
            st.write(message["content"])
            
    chat_input = st.chat_input("How can I assist with your studies today?")
    
    if chat_input:
        st.chat_message("user", avatar="👤").write(chat_input)
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        
        with st.chat_message("assistant", avatar="✦"):
            try:
                prompt = (f"You are NotesAI, a highly intelligent, polite, and deeply analytical AI tutor. "
                          f"You are assisting a 9th-grade student at Neerja studying for the IGCSE exams. "
                          f"Your tone is encouraging and incredibly clear, identical to Claude by Anthropic. "
                          f"Always format your answers beautifully using markdown, bullet points, and bold text for key terms. "
                          f"The current subject focus is: {subject}. \n\n"
                          f"Student's query: {chat_input}")
                
                response = model.generate_content(prompt, stream=True)
                
                def stream_text():
                    for chunk in response:
                        yield chunk.text
                        
                full_response = st.write_stream(stream_text)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                
                st.session_state.xp_points += 5
            except Exception as e:
                st.error(f"System Error: {e}")

    if st.session_state.chat_history:
        st.write("")
        if st.button("Clear Context", key="clear_chat_button"):
            st.session_state.chat_history = []
            st.rerun()

# --- TAB 2: NOTE SCANNER ---
with tab2:
    st.markdown("### Document Digitization")
    st.write("Upload handwritten notes for structural mapping and text extraction.")
    
    uploaded_file = st.file_uploader("Select Image File", type=["jpg", "png", "jpeg"], key="scanner_upload")
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption='Source Document', use_container_width=True)
        
        if st.button("Initialize Vision Analysis", use_container_width=True):
            with st.status("Processing optical data..."):
                try:
                    prompt_msg = "Extract all clear handwritten text from this image. Format it into a highly professional, well-structured academic study guide suitable for 9th-grade IGCSE standards. Use markdown headings and bullet points."
                    response = model.generate_content([prompt_msg, img])
                    
                    st.markdown("---")
                    st.write(response.text)
                    
                    final_download = response.text + "\n\n---\nProcessed by NotesAI"
                    st.download_button(label="Download Document", data=final_download, file_name="NotesAI_Document.txt", mime="text/plain")
                    st.session_state.xp_points += 15
                except Exception as e:
                    st.error(f"Vision API Error: {e}")

# --- TAB 3: QUIZ GENERATOR (NOW STREAMING) ---
with tab3:
    st.markdown("### Formative Assessment Generation")
    topic = st.text_input("Syllabus Topic:", placeholder="e.g., Photosynthesis, The Cold War...")
    diff = st.select_slider("Rigor Level:", options=["Easy", "Medium", "Hard"], value="Medium")
    
    if st.button("Generate Assessment", use_container_width=True):
        if topic:
            try:
                prompt_msg = f"Draft a 5-question multiple choice test focused on '{topic}'. Align it with the expectations of 9th-grade IGCSE criteria at a {diff} level. Maintain a highly professional tone. Provide an answer key at the bottom."
                response = model.generate_content(prompt_msg, stream=True)
                
                st.markdown("---")
                def stream_quiz():
                    for chunk in response:
                        yield chunk.text
                final_quiz = st.write_stream(stream_quiz)
                
                st.download_button(label="Save Assessment", data=final_quiz + "\n\n---\nProcessed by NotesAI", file_name=f"Assessment_{topic}.txt", mime="text/plain")
                st.session_state.xp_points += 15
            except Exception as e:
                st.error(f"Generation Error: {e}")
        else:
            st.warning("Topic field requires input.")

# --- TAB 4: FLASHCARD MAKER (NOW STREAMING) ---
with tab4:
    st.markdown("### Vocabulary & Concept Extraction")
    fc_topic = st.text_input("Target Domain:", placeholder="e.g., Cellular Respiration...")
    
    if st.button("Extract Terminology", use_container_width=True):
        if fc_topic:
            try:
                prompt_msg = f"Create a markdown table with two columns: 'Term' and 'Definition'. Generate 10 highly accurate, essential flashcards for a 9th-grade IGCSE student studying: {fc_topic}."
                response = model.generate_content(prompt_msg, stream=True)
                
                st.markdown("---")
                def stream_cards():
                    for chunk in response:
                        yield chunk.text
                final_cards = st.write_stream(stream_cards)
                
                st.download_button(label="Export Flashcards", data=final_cards + "\n\n---\nProcessed by NotesAI", file_name=f"Flashcards_{fc_topic}.txt", mime="text/plain")
                st.session_state.xp_points += 10
            except Exception as e:
                st.error(f"Generation Error: {e}")
        else:
            st.warning("Domain field requires input.")

# --- TAB 5: ESSAY REVIEWER (NEW!) ---
with tab5:
    st.markdown("### Academic Draft Analysis")
    st.write("Submit an essay or long-form answer for structural and grammatical review based on IGCSE rubrics.")
    essay_text = st.text_area("Paste your draft here:", height=200)
    
    if st.button("Analyze Draft", use_container_width=True):
        if len(essay_text) > 20:
            try:
                prompt_msg = (f"You are a strict but fair IGCSE examiner reviewing a 9th-grade student's draft. "
                              f"Provide a highly structured critique of the following text. "
                              f"Highlight strengths, identify grammatical or logical errors, and suggest vocabulary improvements. "
                              f"Draft: \n\n{essay_text}")
                response = model.generate_content(prompt_msg, stream=True)
                
                st.markdown("---")
                def stream_review():
                    for chunk in response:
                        yield chunk.text
                st.write_stream(stream_review)
                st.session_state.xp_points += 15
            except Exception as e:
                st.error(f"Analysis Error: {e}")
        else:
            st.warning("Please provide a longer draft for accurate analysis.")

# --- 5. THE SECRET TEXT ---
st.markdown('<div class="easter-egg">made by Yuvraj jain</div>', unsafe_allow_html=True)
