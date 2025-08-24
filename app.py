import streamlit as st
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL, MAX_TOKENS, TEMPERATURE
import time
from datetime import datetime

# Check if API key is available
if GOOGLE_API_KEY == "MISSING_API_KEY":
    st.error("""
    🚨 **API Key Missing!**
    
    Your MindSeek app needs a Google Gemini API key to work.
    
    **To fix this:**
    1. Go to your Streamlit Cloud app settings
    2. Add environment variable: `GOOGLE_API_KEY`
    3. Value: Your Gemini API key from [Google AI Studio](https://aistudio.google.com/)
    
    **Or for local development:**
    Create a `.env` file with: `GOOGLE_API_KEY=your_key_here`
    """)
    st.stop()

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel(
    model_name=GEMINI_MODEL,
    generation_config=genai.types.GenerationConfig(
        max_output_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
)

# Function to process messages (defined BEFORE it's used)
def process_message(prompt):
    if not prompt or not prompt.strip():
        return
        
    # Add user message to chat history with timestamp
    current_time = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": current_time,
        "message_id": len(st.session_state.messages) + 1
    })
    st.session_state.chat_count += 1
    
    # Display user message immediately
    display_message("user", prompt, current_time, len(st.session_state.messages))
    
    # Get response from Gemini
    try:
        with st.spinner("🤖 AI is thinking..."):
            response = model.generate_content(prompt)
            
            if response.text:
                # Add assistant message to chat history with timestamp
                response_time = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response.text,
                    "timestamp": response_time,
                    "message_id": len(st.session_state.messages) + 1
                })
                st.session_state.chat_count += 1
                
                # Display assistant response
                display_message("assistant", response.text, response_time, len(st.session_state.messages))
            else:
                st.error("Sorry, I couldn't generate a response. Please try again.")
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.error("There was an error connecting to the AI service. Please check your API key and try again.")

# Function to display messages with enhanced styling
def display_message(role, content, timestamp, message_id):
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message" data-message-id="{message_id}">
            <div class="message-header">
                <div class="user-avatar">👤</div>
                <div class="message-info">
                    <div class="user-name">You</div>
                    <div class="message-time">{timestamp}</div>
                </div>
            </div>
            <div class="user-bubble">
                {content}
            </div>
            <div class="message-actions">
                <button class="action-btn" onclick="copyMessage('{message_id}')" title="Copy message">📋</button>
                <button class="action-btn" onclick="likeMessage('{message_id}')" title="Like message">👍</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message" data-message-id="{message_id}">
            <div class="message-header">
                <div class="ai-avatar">🤖</div>
                <div class="message-info">
                    <div class="ai-name">MindSeek AI</div>
                    <div class="message-time">{timestamp}</div>
                </div>
            </div>
            <div class="bot-bubble">
                {content}
            </div>
            <div class="message-actions">
                <button class="action-btn" onclick="copyMessage('{message_id}')" title="Copy message">📋</button>
                <button class="action-btn" onclick="likeMessage('{message_id}')" title="Like message">👍</button>
                <button class="action-btn" onclick="shareMessage('{message_id}')" title="Share message">📤</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Function to handle input changes (for Enter key)
def on_input_change():
    if st.session_state.get("chat_input"):
        prompt = st.session_state.chat_input.strip()
        if prompt:
            process_message(prompt)
            # Mark that we need to clear input (can't do it here due to Streamlit restrictions)
            st.session_state["clear_input"] = True

# Page configuration
st.set_page_config(
    page_title="MindSeek - AI Chat Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for ChatGPT-style interface with avatars and timestamps
st.markdown("""
<style>
    /* Modern Chat Interface Styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .chat-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        min-height: 500px;
    }
    
    /* Enhanced Message Styling with Avatars and Timestamps */
    .chat-message {
        margin: 2rem 0;
        animation: fadeInUp 0.6s ease-out;
        position: relative;
    }
    
    .chat-message:not(:last-child)::after {
        content: '';
        position: absolute;
        bottom: -1rem;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Message Header with Avatar and Info */
    .message-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
        padding: 0.5rem 0;
    }
    
    .user-avatar, .ai-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        flex-shrink: 0;
    }
    
    .user-avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .ai-avatar {
        background: linear-gradient(135deg, #00d4aa 0%, #0099cc 100%);
        color: white;
    }
    
    .message-info {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    
    .user-name, .ai-name {
        font-weight: 600;
        font-size: 14px;
        color: #2c3e50;
    }
    
    .message-time {
        font-size: 12px;
        color: #6c757d;
        font-weight: 500;
    }
    
    /* Enhanced Message Bubbles */
    .user-message {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        margin-bottom: 1.5rem;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.25rem 1.5rem;
        border-radius: 25px 25px 5px 25px;
        max-width: 85%;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.25);
        position: relative;
        animation: slideInRight 0.5s ease-out;
        word-wrap: break-word;
        line-height: 1.6;
        font-size: 15px;
    }
    
    .user-bubble::before {
        content: '';
        position: absolute;
        right: -8px;
        top: 20px;
        width: 0;
        height: 0;
        border-left: 10px solid #764ba2;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .bot-message {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-bottom: 1.5rem;
    }
    
    .bot-bubble {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        color: #2c3e50;
        padding: 1.25rem 1.5rem;
        border-radius: 25px 25px 25px 5px;
        max-width: 85%;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
        position: relative;
        animation: slideInLeft 0.5s ease-out;
        word-wrap: break-word;
        line-height: 1.6;
        white-space: pre-wrap;
        font-size: 15px;
    }
    
    .bot-bubble::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 20px;
        width: 0;
        height: 0;
        border-right: 10px solid #ffffff;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Message Action Buttons */
    .message-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.75rem;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .chat-message:hover .message-actions {
        opacity: 1;
    }
    
    .action-btn {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 0.75rem;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .action-btn:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* ChatGPT-Style Enhanced Input Area */
    .chat-input-container {
        background: rgba(255,255,255,0.95);
        border-radius: 25px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        border: 2px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(15px);
        margin-top: 2rem;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .chat-input-container:hover {
        box-shadow: 0 12px 40px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    .chat-input-container:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
    }
    
    .input-wrapper {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: #f8f9fa;
        border-radius: 20px;
        padding: 0.5rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .input-wrapper:focus-within {
        background: white;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stTextInput > div > div > input {
        border: none !important;
        background: transparent !important;
        border-radius: 15px !important;
        padding: 1rem 1.5rem !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        color: #2c3e50 !important;
        transition: all 0.3s ease !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: none !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6c757d !important;
        font-weight: 400 !important;
    }
    
    .send-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        font-size: 18px;
    }
    
    .send-button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .send-button:active {
        transform: scale(0.95);
    }
    
    .input-actions {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .action-button {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 16px;
    }
    
    .action-button:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: scale(1.05);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Enhanced Sidebar */
    .sidebar-content {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .user-bubble, .bot-bubble {
            max-width: 90%;
        }
        .main-header {
            padding: 1.5rem;
        }
        .chat-input-container {
            padding: 1rem;
        }
        .message-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
        }
    }
    
    /* Scrollbar Styling */
    .main .block-container {
        scrollbar-width: thin;
        scrollbar-color: #667eea #f1f1f1;
    }
    
    .main .block-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .main .block-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .main .block-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    .main .block-container::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* JavaScript for action buttons */
    <script>
    function copyMessage(messageId) {
        const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
        const messageText = messageElement.querySelector('.user-bubble, .bot-bubble').textContent;
        navigator.clipboard.writeText(messageText).then(() => {
            // Show copy success
            const btn = event.target;
            btn.textContent = '✅';
            setTimeout(() => btn.textContent = '📋', 2000);
        });
    }
    
    function likeMessage(messageId) {
        const btn = event.target;
        btn.textContent = '❤️';
        btn.style.background = 'rgba(255, 105, 180, 0.2)';
        btn.style.color = '#ff69b4';
    }
    
    function shareMessage(messageId) {
        const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
        const messageText = messageElement.querySelector('.user-bubble, .bot-bubble').textContent;
        if (navigator.share) {
            navigator.share({
                title: 'MindSeek Chat',
                text: messageText
            });
        } else {
            // Fallback to clipboard
            navigator.clipboard.writeText(messageText);
            const btn = event.target;
            btn.textContent = '✅';
            setTimeout(() => btn.textContent = '📤', 2000);
        }
    }
    </script>
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

# Enhanced Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #667eea; font-size: 2rem; margin: 0;">🧠 MindSeek</h1>
        <p style="color: #666; margin: 0;">AI Chat Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model selection
    st.markdown("### 🚀 AI Model")
    model_option = st.selectbox(
        "Choose Model:",
        ["gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
        label_visibility="collapsed"
    )
    
    # Temperature slider
    st.markdown("### 🎭 Creativity Level")
    temperature = st.slider(
        "Creativity Level:",
        min_value=0.0,
        max_value=1.0,
        value=TEMPERATURE,
        step=0.1,
        help="Lower values = more focused, Higher values = more creative",
        label_visibility="collapsed"
    )
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_count = 0
        st.rerun()
    
    # Chat statistics
    st.markdown("### 📊 Chat Statistics")
    st.markdown(f"""
    <div class="stats-card">
        <h3 style="margin: 0; font-size: 1.5rem;">{st.session_state.chat_count}</h3>
        <p style="margin: 0; opacity: 0.9;">Total Messages</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Current Model:** {model_option}")
    
    # About section
    st.markdown("### ℹ️ About")
    st.markdown("**Powered by Google Gemini AI**")
    st.markdown("**Built with ❤️ using Streamlit**")

# Enhanced Main Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 3rem; font-weight: 700;">🧠 MindSeek</h1>
    <p style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Your Intelligent AI Chat Assistant</p>
    <p style="margin: 0; font-size: 1rem; opacity: 0.8;">Powered by Google Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# Enhanced Chat Interface
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages with enhanced styling
    for message in st.session_state.messages:
        display_message(message["role"], message["content"], message["timestamp"], message["message_id"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle input clearing after message sent
    if st.session_state.get("clear_input"):
        st.session_state.chat_input = ""
        st.session_state["clear_input"] = False
    
    # ChatGPT-Style Enhanced Chat Input
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    
    # Create columns for input and buttons
    col1, col2, col3 = st.columns([4, 1, 1])
    
    with col1:
        # Enhanced input field with ENTER key support using on_change
        prompt = st.text_input(
            "Ask me anything...",
            key="chat_input",
            placeholder="Type your message here... (Press Enter to send)",
            label_visibility="collapsed",
            on_change=on_input_change
        )
    
    with col2:
        # File attachment button (functional)
        if st.button("📎", key="file_button", help="Attach file (coming soon)"):
            st.info("📎 File attachment feature coming in the next update!")
    
    with col3:
        # Send button with professional send icon
        if st.button("📤", key="send_button", help="Send message"):
            if prompt and prompt.strip():
                process_message(prompt)
                # Mark that we need to clear input
                st.session_state["clear_input"] = True
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin-top: 2rem;'>
    <p style="margin: 0; font-size: 1.1rem; font-weight: 600;">🧠 MindSeek - Powered by Google Gemini AI</p>
    <p style="margin: 0.5rem 0; opacity: 0.8;">Built with ❤️ using Streamlit</p>
    <p style="margin: 0; font-size: 0.9rem; opacity: 0.7;">Last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)


