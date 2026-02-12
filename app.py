import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# 1. API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets!")

model = genai.GenerativeModel('gemini-2.0-flash')

# 2. THE CHATGPT DARK UI & ANIMATION
st.set_page_config(page_title="NotesAI | Studio", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* ChatGPT Dark Background */
    .stApp {
        background-color: #212121;
        color: #ececec;
    }
    
    /* Center the main content area */
    .block-container {
        max-width: 800px;
        padding-top: 2rem;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #171717 !important;
    }

    /* Custom 'Study-Thinking' Animation */
    @keyframes rotateSymbols {
        0% { transform: rotate(0deg); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: rotate(360deg); opacity: 0; }
    }
    .thinking-container {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 10px;
        color: #ab9ff2;
        font-family: monospace;
    }
    .math-icon {
        font-size: 24px;
        animation: rotateSymbols 2s linear infinite;
    }

    /* Input Box Styling */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Define the custom thinking animation as a function
def study_spinner():
    return st.markdown("""
        <div class="thinking-container">
            <div class="math-icon">π</div>
            <div class="math-icon" style="animation-delay: 0.5s">H₂O</div>
            <div class="math-icon" style="animation-delay: 1s">Σ</div>
            <span>NotesAI is analyzing equations...</span>
        </div>
    """, unsafe_allow_html=True)

# --- APP LAYOUT ---
st.title("⚡ NotesAI")
st.markdown("---")

# Sidebar
st.sidebar.title("NotesAI Tools")
mode = st.sidebar.radio("Switch View", ["💬 Tutor Chat", "📷 Scanner", "📝 Quiz Builder"])

GEMINI_LOGO = "https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d47353047313511b7d3f2.svg"

# 3. MODE LOGIC
if mode == "💬 Tutor Chat":
    chat_input = st.chat_input("Ask NotesAI anything...")
    
    if chat_input:
        st.chat_message("user").write(chat_input)
        
        # Trigger the custom "Thinking" animation
        thinking_placeholder = st.empty()
        with thinking_placeholder:
            study_spinner()
            
        try:
            # Generate response
            response = model.generate_content(f"You are NotesAI, a professional 8th grade tutor. Explain: {chat_input}")
            
            # Remove animation and show answer
            thinking_placeholder.empty()
            with st.chat_message("assistant", avatar=GEMINI_LOGO):
                st.markdown("**NotesAI**")
                st.write(response.text)
        except Exception as e:
            thinking_placeholder.empty()
            st.error(f"Error: {e}")

# (Note: Keep Scanner and Quiz logic from previous code here)
