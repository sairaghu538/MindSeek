import streamlit as st
from google import genai
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
# Configure Gemini Client
client = genai.Client(api_key=GOOGLE_API_KEY)

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
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    max_output_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                )
            )
            
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
def display_message(role, content, timestamp=None, message_id=None):
    # Handle old message format (without timestamp/message_id)
    if timestamp is None:
        timestamp = "Now"
    if message_id is None:
        message_id = "msg_" + str(time.time())
    
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
    /* Global Settings & Dark Theme */
    .stApp {
        background-color: #0e1117;
        background-image: radial-gradient(circle at 50% 0%, #1c2029 0%, #0e1117 100%);
        color: #fafafa;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #161b24;
        border-right: 1px solid #2d3748;
    }
    
    [data-testid="stSidebar"] h1 {
        color: #fff;
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #a0aec0;
    }
    
    /* Main Header Styling */
    .main-header {
        background: transparent;
        padding: 1rem 0 3rem 0;
        text-align: left;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #fff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #94a3b8;
        font-size: 1.2rem;
        font-weight: 400;
    }

    /* Card-like Containers */
    .chat-container {
        background-color: #1e2530;
        border: 1px solid #2d3748;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Message Bubbles - Dark Mode Premium */
    .user-message {
        align-items: flex-end;
        margin-bottom: 1.5rem;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); /* Indigo to Purple */
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 16px 16px 2px 16px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        max-width: 80%;
        line-height: 1.6;
    }
    
    .bot-message {
        align-items: flex-start;
        margin-bottom: 1.5rem;
    }
    
    .bot-bubble {
        background-color: #2d3748;
        color: #e2e8f0;
        padding: 1rem 1.5rem;
        border-radius: 16px 16px 16px 2px;
        border: 1px solid #4a5568;
        max-width: 80%;
        line-height: 1.6;
    }
    
    /* Avatar Styling */
    .user-avatar {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        width: 36px;
        height: 36px;
        font-size: 18px;
    }
    
    .ai-avatar {
        background: #4a5568;
        color: #a5b4fc;
        width: 36px;
        height: 36px;
        font-size: 18px;
    }
    
    /* Input Area - Control Center Style */
    .chat-input-container {
        background-color: #161b24;
        border: 1px solid #2d3748;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 2rem;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
    }
    
    .stTextInput input {
        background-color: #0e1117 !important;
        color: #fff !important;
        border: 1px solid #2d3748 !important;
        border-radius: 8px !important;
        padding: 0.8rem 1rem !important;
    }
    
    .stTextInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Buttons - Neon Actions */
    .stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.5);
    }
    
    /* Selectbox customization for dark mode */
    div[data-baseweb="select"] > div {
        background-color: #0e1117;
        color: white;
        border-color: #2d3748;
    }
    
    div[data-baseweb="popover"] {
        background-color: #1a202c;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background: #0e1117;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2d3748;
        border-radius: 5px;
    }

    /* Helper utility to hide Streamlit branding if desired */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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
        <h1 style="font-size: 2rem; margin: 0;">🧠 MindSeek</h1>
        <p style="margin: 0;">AI Chat Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model selection
    st.markdown("### 🚀 AI Model")
    model_option = st.selectbox(
        "Choose Model:",
        ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
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
    
    # Debug Section
    with st.expander("🛠️ Debug Info"):
        try:
            st.write(f"SDK Version: {genai.__version__}")
        except:
            st.write("SDK Version: Unknown")
            
        if st.button("List Available Models"):
            try:
                models = client.models.list()
                for m in models:
                    st.code(m.name)
            except Exception as e:
                st.error(f"Error listing models: {e}")

# Enhanced Main Header
st.markdown("""
<div class="main-header">
    <h1>🧠 MindSeek</h1>
    <p>Your Intelligent AI Chat Assistant</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.6;">Powered by Google Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# Enhanced Chat Interface
chat_container = st.container()

with chat_container:

    
    # Display chat messages with enhanced styling
    for message in st.session_state.messages:
        # Handle both old and new message formats
        timestamp = message.get("timestamp", "Now")
        message_id = message.get("message_id", f"msg_{len(st.session_state.messages)}")
        display_message(message["role"], message["content"], timestamp, message_id)
    
    # Handle input clearing after message sent
    if st.session_state.get("clear_input"):
        st.session_state.chat_input = ""
        st.session_state["clear_input"] = False
    
    # ChatGPT-Style Enhanced Chat Input

    
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

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin-top: 2rem;'>
    <p style="margin: 0; font-size: 1.1rem; font-weight: 600;">🧠 MindSeek - Powered by Google Gemini AI</p>
    <p style="margin: 0.5rem 0; opacity: 0.8;">Built with ❤️ using Streamlit</p>
    <p style="margin: 0; font-size: 0.9rem; opacity: 0.7;">Last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)


