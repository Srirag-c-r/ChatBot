import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
from chatbot import MultiLanguageChatbot

# Page configuration
st.set_page_config(
    page_title="🌍 Multi-Language AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the chatbot
@st.cache_resource
def load_chatbot():
    return MultiLanguageChatbot()

def init_database():
    """Initialize SQLite database for chat history"""
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_message TEXT,
            bot_response TEXT,
            detected_language TEXT,
            translated_message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_conversation(user_msg, bot_response, detected_lang, translated_msg):
    """Save conversation to database"""
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO conversations (timestamp, user_message, bot_response, detected_language, translated_message)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), user_msg, bot_response, detected_lang, translated_msg))
    conn.commit()
    conn.close()

def load_chat_history():
    """Load chat history from database"""
    conn = sqlite3.connect('chat_history.db')
    df = pd.read_sql_query("SELECT * FROM conversations ORDER BY timestamp DESC LIMIT 50", conn)
    conn.close()
    return df

def main():
    # Initialize database
    init_database()
    
    # Load chatbot
    chatbot = load_chatbot()
    
    # Header
    st.title("🌍 Multi-Language AI Chatbot")
    st.markdown("**Chat in any language - I'll understand and respond intelligently!**")
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Settings")
        
        # Language selection
        target_language = st.selectbox(
            "Response Language:",
            ["auto", "english", "spanish", "french", "german", "italian", "portuguese", 
             "russian", "chinese", "japanese", "korean", "arabic", "hindi"]
        )
        
        # Model selection
        model_option = st.selectbox(
            "Chatbot Model:",
            ["DialoGPT (Fast)", "BlenderBot (Better)", "FLAN-T5 (Instruction)"]
        )
        
        # Translation option
        enable_translation = st.checkbox("Enable Translation", value=True)
        
        st.markdown("---")
        
        # Chat history
        st.header("📚 Recent Chats")
        if st.button("Clear History"):
            conn = sqlite3.connect('chat_history.db')
            c = conn.cursor()
            c.execute("DELETE FROM conversations")
            conn.commit()
            conn.close()
            st.success("History cleared!")
            st.rerun()
        
        # Show recent conversations
        history_df = load_chat_history()
        if not history_df.empty:
            for _, row in history_df.head(5).iterrows():
                with st.expander(f"🕒 {row['timestamp'][:16]}"):
                    st.write(f"**You ({row['detected_language']}):** {row['user_message'][:100]}...")
                    st.write(f"**Bot:** {row['bot_response'][:100]}...")
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat container
        chat_container = st.container()
        
        # Initialize session state
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if "metadata" in message:
                        st.caption(message["metadata"])
        
        # Chat input
        if prompt := st.chat_input("Type your message in any language..."):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Process with chatbot
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    # Detect language
                    detected_lang = chatbot.detect_language(prompt)
                    
                    # Translate if needed
                    translated_prompt = prompt
                    if enable_translation and detected_lang != 'en':
                        translated_prompt = chatbot.translate_text(prompt, 'en')
                    
                    # Generate response
                    response = chatbot.generate_response(translated_prompt, model_option)
                    
                    # Translate response back if needed
                    final_response = response
                    if enable_translation and target_language != "auto" and target_language != "english":
                        final_response = chatbot.translate_text(response, target_language)
                    
                    # Display response
                    st.markdown(final_response)
                    
                    # Show metadata
                    metadata = f"🔍 Detected: {detected_lang} | 🎯 Model: {model_option}"
                    if enable_translation:
                        metadata += f" | 🌐 Translated"
                    st.caption(metadata)
                    
                    # Save to session and database
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": final_response,
                        "metadata": metadata
                    })
                    
                    save_conversation(prompt, final_response, detected_lang, translated_prompt)
    
    with col2:
        st.header("🎯 Features")
        st.markdown("""
        ✅ **Language Detection**  
        ✅ **Smart Translation**  
        ✅ **Context Awareness**  
        ✅ **Chat History**  
        ✅ **Multiple Models**  
        ✅ **50+ Languages**  
        """)
        
        st.header("🌍 Supported Languages")
        languages = [
            "🇺🇸 English", "🇪🇸 Spanish", "🇫🇷 French", "🇩🇪 German",
            "🇮🇹 Italian", "🇵🇹 Portuguese", "🇷🇺 Russian", "🇨🇳 Chinese",
            "🇯🇵 Japanese", "🇰🇷 Korean", "🇸🇦 Arabic", "🇮🇳 Hindi",
            "And 40+ more!"
        ]
        for lang in languages:
            st.markdown(f"• {lang}")

if __name__ == "__main__":
    main()
