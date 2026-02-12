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
    /* Style for the cards */
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
    # Adding a professional study-themed image to the sidebar
    st.image("https://img.freepik.com/free-vector/online-education-concept-illustration_114360-8422.jpg", use_container_width=True)
    st.header("📌 Navigation")
    mode = st.selectbox("Choose a Study Mode", ["Tutor Chat", "Note Scanner", "Exam Prep (Quiz)"])
    st.divider()
    st.markdown("### 🛠️ App Stats")
    st.caption("Model: Gemini 2.5 Flash")
    st.caption("Status: Online 🟢")

# --- MAIN CONTENT GRAPHICS ---
col1, col2 = st.columns([1, 4])
with col1:
    # A smaller logo/icon next to the title
    st.image("https://cdn-icons-png.flaticon.com/512/5190/5190714.png", width=80)
with col2:
    st.title("NotesAI")
    st.subheader("Your Intelligent STEM Study Partner")

# Feature Description using a styled container
st.markdown("""
<div class="feature-card">
    <strong>Welcome to the future of studying!</strong><br>
    NotesAI uses advanced Generative AI to act as your personal tutor. Whether you're preparing for 
    your 8th-grade finals or just curious about Chemistry, we've got you covered.
</div>
""", unsafe_allow_html=True)

st.divider()

# 3. Mode Logic
if mode == "Tutor Chat":
    st.markdown("### 💬 Interactive Tutor")
    st.info("Tip: Ask about the 'Revolt of 1857' or 'Rate of Chemical Reactions'!")
    chat_input = st.chat_input("Type your question here...")
    if chat_input:
        with st.spinner("NotesAI is thinking..."):
            try:
                response = model.generate_content(f"You are NotesAI, a helpful academic tutor. Explain this clearly for an 8th grader: {chat_input}")
                st.chat_message("assistant", avatar="🎓").write(response.text)
            except Exception as e:
                st.error(f"AI Error: {e}")

elif mode == "Note Scanner":
    st.markdown("### 📸 Vision Scanner")
    st.info("NotesAI can read handwritten text and organize it into study points.")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        # Using columns to show image and summary side-by-side
        img_col, text_col = st.columns(2)
        with img_col:
            st.image(img, caption='Uploaded Notes', use_container_width=True)
        
        with text_col:
            if st.button("✨ Analyze & Summarize"):
                with st.spinner("NotesAI is reading your handwriting..."):
                    try:
                        response = model.generate_content(["Read this image. Transcribe the text and provide a structured summary with key points.", img])
                        st.success("Analysis Complete!")
                        st.markdown("---")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"AI Error: {e}")

elif mode == "Exam Prep (Quiz)":
    st.markdown("### 📝 Quiz Generator")
    st.info("Test your knowledge! Enter any topic to generate a custom 5-question test.")
    topic = st.text_input("Enter Topic (e.g., '1857 Revolt')", placeholder="Type here...")
    
    if st.button("🔥 Generate 5-Question Quiz"):
        with st.spinner("Creating your quiz..."):
            try:
                response = model.generate_content(f"Generate a 5-question multiple choice quiz on {topic} for an 8th-grade student. Include answers at the end.")
                st.balloons() # Adding a fun graphic effect
                st.markdown("### ❓ Practice Quiz")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI Error: {e}")
