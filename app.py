# --- TAB 1: INTERACTIVE TUTOR (CLAUDE-STYLE) ---
with tab1:
    st.markdown("### 💬 Real-Time IGCSE Tutor Chat")
    
    subject = st.radio("Focus Area:", ["General", "Science", "History", "Math", "English"], horizontal=True)
    
    # Display previous messages
    for message in st.session_state.chat_history:
        # Using a sleek, minimalist style (no emojis for the user, professional icon for AI)
        with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
            st.write(message["content"])
            
    chat_input = st.chat_input("Ask a question (e.g., 'Can you explain the carbon cycle?')...")
    
    if chat_input:
        # 1. Print user message
        st.chat_message("user", avatar="👤").write(chat_input)
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        
        # 2. Generate Claude-style Streaming Response
        with st.chat_message("assistant", avatar="🤖"):
            try:
                # The "Claude" Persona Prompt
                prompt = (
                    f"You are NotesAI, a highly intelligent, polite, and helpful AI tutor. "
                    f"You are assisting a 9th-grade student at Neerja studying for the IGCSE exams. "
                    f"Your tone should be encouraging and incredibly clear, similar to Claude by Anthropic. "
                    f"Always format your answers beautifully using markdown, bullet points, and bold text for key terms. "
                    f"The current subject focus is: {subject}. \n\n"
                    f"Student's question: {chat_input}"
                )
                
                # Turn on streaming!
                response = model.generate_content(prompt, stream=True)
                
                # Create a generator to stream the text chunks directly to the UI
                def stream_text():
                    for chunk in response:
                        yield chunk.text
                
                # Write the stream to the screen (creates that typing effect!)
                full_response = st.write_stream(stream_text)
                
                # Save the full final response to memory
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                
                # Gamification
                st.session_state.xp_points += 5
                st.toast("🎉 +5 XP for an excellent question!")
                
            except Exception as e:
                st.error(f"AI System Error: {e}")

    # Clean clear chat button
    if st.session_state.chat_history:
        st.write("")
        if st.button("✨ Start New Conversation", key="clear_chat_button"):
            st.session_state.chat_history = []
            st.rerun()
