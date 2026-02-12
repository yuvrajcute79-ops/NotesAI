import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets!")

model = genai.GenerativeModel('gemini-2.0-flash')

# 2. UI STYLING (The Black Bar + Clickable Pill)
st.set_page_config(page_title="NotesAI", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #f0f2f6; }

    /* The Rounded Black Input Container Style */
    div[data-testid="stChatInput"] {
        background-color: #2f2f2f !important;
        border: 1.5px solid #ff7066 !important;
        border-radius: 25px !important;
        padding: 5px 15px !important;
    }

    /* Styling for the clickable mode pills */
    .st-emotion-cache-18ni7ap { display: none; } /* Hide default sidebar if you want it all in the bar */
    
    .pill-container {
        display: flex;
        align-items: center;
        background-color: #2f2f2f;
        padding: 10px 20px;
        border-radius: 25px 25px 0 0;
        border: 1.5px solid #ff7066;
        border-bottom: none;
        width: fit-content;
        margin-left: 20px;
        gap: 15px;
    }
    
    .tool-label { color: white; font-weight: bold; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SELECTABLE PILL MENU (Using Streamlit's native buttons styled as pills)
st.title("🎓 NotesAI")
st.markdown("Select your study tool and type your request below.")

# Horizontal Menu (This acts as your clickable 'Fast' switcher)
col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
with col1:
    st.markdown("**+ Tools**")
with col2:
    if st.button("💬 Tutor Chat"): st.session_state.mode = "Tutor Chat"
with col3:
    if st.button("📸 Note Scanner"): st.session_state.mode = "Note Scanner"
with col4:
    if st.button("📝 Quiz Practice"): st.session_state.mode = "Quiz Practice"

# Default Mode
if 'mode' not in st.session_state:
    st.session_state.mode = "Tutor Chat"

current_mode = st.session_state.mode
st.info(f"Currently using: **{current_mode}**")

# 4. CHAT & TOOL LOGIC
if current_mode == "Tutor Chat":
    chat_input = st.chat_input(f"Type your question for {current_mode}...")
    if chat_input:
        with st.chat_message("assistant"):
            st.write(model.generate_content(chat_input).text)

elif current_mode == "Note Scanner":
    uploaded_file = st.file_uploader("Upload Notes", type=["jpg", "png", "jpeg"])
    chat_input = st.chat_input("Ask something about the notes above...")
    if uploaded_file and chat_input:
        img = Image.open(uploaded_file)
        st.write(model.generate_content([chat_input, img]).text)

elif current_mode == "Quiz Practice":
    chat_input = st.chat_input("Enter topic to generate quiz...")
    if chat_input:
        st.write(model.generate_content(f"Generate 5 quiz questions on {chat_input}").text)
