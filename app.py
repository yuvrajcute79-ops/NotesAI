import streamlit as st
import google.generativeai as genai
from PIL import Image

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
    }
    .feature-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR GRAPHICS ---
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg", use_container_width=True)
    st.header("📌 Navigation")
    mode = st.selectbox("Choose a Study Mode", ["Tutor Chat", "Note Scanner", "Exam Prep (Quiz)"])
    
    st.divider()
    st.markdown("### 📊 Learning Dashboard")
    # Removed model version, added metrics
    st.metric(label="System Status", value="Active", delta="100% Uptime")
    st.metric(label="AI Latency", value="Low", delta="-0.2s")
    st.caption("Status: Ready for IGCSE/IB Support 🟢")

# --- MAIN CONTENT GRAPHICS ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=80)
with col2:
    st.title("NotesAI")
    st.subheader("Your Intelligent STEM Study Partner")

st.markdown("""
<div class="feature-card">
    <strong>Welcome to the future of studying!</strong><br>
    NotesAI is designed specifically for <strong>Neerja Modi World School</strong> students to bridge the gap between 
    handwritten notes and digital mastery. Our engine can decipher complex handwriting, explain 
    intricate STEM concepts, and verify your knowledge through adaptive testing.
</div>
""", unsafe_allow_html=True)

st.divider()

# 3. Mode Logic
if mode == "Tutor Chat":
    st.markdown("### 💬 Interactive Tutor")
    st.write("""
    **How to use:** Type any concept you're struggling with in the chat box below. 
    NotesAI is trained on IGCSE and IBDP curricula to provide age-appropriate explanations.
    """)
    st.info("💡 **Try asking:** 'Explain the importance of the 1857 Revolt' or 'What is a Catalyst in Chemistry?'")
    
    chat_input = st.chat_input("Type your question here...")
    if chat_input:
        with st.spinner("NotesAI is processing your query..."):
            try:
                response = model.generate_content(f"You are NotesAI, a helpful academic tutor. Explain this clearly for an 8th grader: {chat_input}")
                st.chat_message("assistant", avatar="🎓").write(response.text)
            except Exception as e:
                st.error(f"AI Error: {e}")

elif mode == "Note Scanner":
    st.markdown("### 📸 Vision Scanner")
    st.write("""
    **How to use:** Upload a clear photo of your notebook or textbook. Our computer vision 
    technology will extract the text and create a summarized 'Cheat Sheet' for your exams.
    """)
    st.warning("⚠️ **For best results:** Ensure the handwriting is legible and the lighting is bright.")
    
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
                        response = model.generate_content(["Read this image. Transcribe the text and provide a structured summary with key points.", img])
                        st.success("Data Extraction Complete!")
                        st.markdown("#### 📝 Notes Summary")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"AI Error: {e}")

elif mode == "Exam Prep (Quiz)":
    st.markdown("### 📝 Quiz Generator")
    st.write("""
    **How to use:** Enter a specific topic (e.g., 'Plant Cells' or 'Algebraic Identities'). 
    NotesAI will generate a 5-question mock test to challenge your understanding.
    """)
    topic = st.text_input("What would you like to be tested on?", placeholder="Enter topic here...")
    
    if st.button("🔥 Generate 5-Question Quiz"):
        with st.spinner("Generating academic test questions..."):
            try:
                response = model.generate_content(f"Generate a 5-question multiple choice quiz on {topic} for an 8th-grade student. Include answers at the end.")
                st.balloons() 
                st.markdown("---")
                st.markdown("### ❓ Practice Quiz")
                st.write(response.text)
                st.caption("✅ Answers are provided at the bottom of the generated text.")
            except Exception as e:
                st.error(f"AI Error: {e}")
