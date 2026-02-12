import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets!")

# Model Selection - 1.5-flash is best for high-traffic free tier use
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. UI BRANDING & CUSTOM CSS
st.set_page_config(page_title="NotesAI | NMWS Hub", page_icon="🎓", layout="wide")

# --- CUSTOM LOGO SETUP ---
# Update this link with your actual logo file path later
NOTES_AI_LOGO = "https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d47353047313511b7d3f2.svg" 

st.markdown(f"""
    <style>
    /* Main Background */
    .stApp {{ background-color: #f0f2f6; }}
    
    /* Sidebar: Navy Blue */
    section[data-testid="stSidebar"] {{
        background-color: #002366 !important;
        color: white;
    }}
    section[data-testid="stSidebar"] .stMarkdown h1, h2, h3, p {{
        color: white !important;
    }}

    /* Buttons: Professional Navy */
    div.stButton > button:first-child {{
        background-color: #002366;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        height: 3.5em;
        width: 100%;
        border: none;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }}
    
    /* Input field focus */
    .stChatInputContainer {{ padding-bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR & NAVIGATION ---
st.sidebar.title("⚡ NotesAI")
st.sidebar.markdown("NMWS STEM Exhibition 2026")
st.sidebar.markdown("---")
mode = st.sidebar.radio("CHOOSE TOOL:", ["🧠 24/7 Personal Tutor", "📸 Smart Note Scanner", "📝 Instant Quiz Maker"])

# --- MAIN CONTENT ---
st.title(f"🎓 {mode}")

if mode == "🧠 24/7 Personal Tutor":
    st.info("Ask NotesAI about your IGCSE or IB syllabus topics.")
    chat_input = st.chat_input("Ask a question...")
    
    if chat_input:
        st.chat_message("user").write(chat_input)
        
        with st.spinner("NotesAI is processing your query..."):
            try:
                with st.chat_message("assistant", avatar=NOTES_AI_LOGO):
                    st.markdown("**NotesAI**")
                    response = model.generate_content(f"You are NotesAI, a professional tutor for an 8th grade student. Explain: {chat_input}")
                    st.write(response.text)
            except Exception as e:
                # This handles the Quota Exceeded error gracefully
                if "429" in str(e):
                    st.error("⚠️ **NotesAI is currently busy (Rate Limit).** Please wait 60 seconds and try again. This happens because we are on the Free Tier!")
                else:
                    st.error(f"Error: {e}")

elif mode == "📸 Smart Note Scanner":
    st.write("Upload your handwritten notes for an instant AI summary.")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        col1, col2 = st.columns(2)
        with col1:
            img = Image.open(uploaded_file)
            st.image(img, caption='Your Notes', use_container_width=True)
        with col2:
            if st.button("Summarize with NotesAI"):
                with st.spinner("Analyzing..."):
                    try:
                        response = model.generate_content(["Convert these handwritten notes into clear study points.", img])
                        st.success("Summary Ready!")
                        st.write(response.text)
                    except Exception as e:
                        if "429" in str(e):
                            st.error("⚠️ Rate Limit reached. Wait 60s.")
                        else:
                            st.error(f"Error: {e}")

elif mode == "📝 Instant Quiz Maker":
    topic = st.text_input("Enter topic for your quiz:", placeholder="e.g. French Revolution")
    if st.button("Generate Quiz"):
        with st.spinner("Creating questions..."):
            try:
                response = model.generate_content(f"Create a 5 question quiz for 8th grade on {topic}. Include answers at the bottom.")
                st.write(response.text)
            except Exception as e:
                if "429" in str(e):
                    st.error("⚠️ Rate Limit reached. Wait 60s.")
                else:
                    st.error(f"Error: {e}")
