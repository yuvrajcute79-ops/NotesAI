import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets!")

# Model Selection
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 2. ADVANCED UI CUSTOMIZATION
st.set_page_config(page_title="NotesAI", page_icon="🎓", layout="wide")

# Custom CSS to match the image you sent
st.markdown("""
    <style>
    /* Dark Theme for Input area */
    .stChatInputContainer {
        padding: 20px;
        background-color: transparent;
    }
    
    /* The Rounded Black Input Bar */
    div[data-testid="stChatInput"] {
        background-color: #2f2f2f !important;
        border: 1.5px solid #ff7066 !important; /* The red border from your pic */
        border-radius: 25px !important;
        padding: 10px 15px !important;
    }

    /* Styling the placeholder text */
    textarea[data-testid="stChatInputTextArea"] {
        color: #ffffff !important;
    }

    /* "Tools" and Mode Labels inside the bar */
    .input-tools-overlay {
        display: flex;
        align-items: center;
        gap: 10px;
        padding-top: 5px;
        font-family: sans-serif;
    }
    .tool-plus { color: #ffffff; font-size: 20px; font-weight: bold; }
    .tool-text { color: #bbbbbb; font-size: 14px; }
    .mode-pill {
        background-color: #3e3e3e;
        color: white;
        padding: 2px 12px;
        border-radius: 15px;
        font-size: 12px;
        border: 1px solid #555;
    }
    .mode-dot { color: #448aff; margin-left: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
st.sidebar.title("⚡ NotesAI")
st.sidebar.markdown("NMWS STEM Project 2026")
st.sidebar.markdown("---")
mode = st.sidebar.radio("SWITCH MODE:", ["Tutor Chat", "Note Scanner", "Quiz Practice"])

# --- MAIN UI ---
st.title("🎓 NotesAI")
st.markdown("Your all-in-one AI study partner for simplifying topics and mastering exams.")

# Creating the visual "Tools" overlay that mimics your image
st.markdown(f"""
    <div class="input-tools-overlay">
        <span class="tool-plus">+</span>
        <span class="tool-text">Tools</span>
        <div class="mode-pill">{mode}<span class="mode-dot">●</span></div>
    </div>
    """, unsafe_allow_html=True)

# 4. CHAT LOGIC
if mode == "Tutor Chat":
    chat_input = st.chat_input("Type your question here...")
    if chat_input:
        st.chat_message("user").write(chat_input)
        with st.spinner("NotesAI is thinking..."):
            response = model.generate_content(f"Explain this clearly for an 8th grader: {chat_input}")
            with st.chat_message("assistant"):
                st.markdown("**NotesAI**")
                st.write(response.text)

elif mode == "Note Scanner":
    st.info("Upload notes to summarize.")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if uploaded_file and st.button("Summarize"):
        img = Image.open(uploaded_file)
        response = model.generate_content(["Summarize these notes:", img])
        st.write(response.text)

elif mode == "Quiz Practice":
    topic = st.text_input("Enter Topic")
    if st.button("Generate Quiz"):
        response = model.generate_content(f"Create a 5 question quiz on {topic}")
        st.write(response.text)
