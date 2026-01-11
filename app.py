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
    /* Glassmorphism Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Glass Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Modern Glass Headers */
    .main-header {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(15px);
        padding: 2.5rem;
        border-radius: 20px;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Glass Chat Container */
    .chat-container {
        background: rgba(255, 255, 255, 0.25);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        backdrop-filter: blur(4px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem;
        min-height: 500px;
    }
    
    /* Input Container Glass */
    .chat-input-container {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.6);
        margin-top: 2rem;
    }
    
    /* Inputs & Selectboxes */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.1);
        backdrop-filter: blur(4px);
    }
    
    /* Sliders */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    /* Message Bubbles */
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.25rem 1.5rem;
        border-radius: 20px 20px 0 20px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        max-width: 85%;
        margin-left: auto;
    }
    
    .bot-bubble {
        background: rgba(255, 255, 255, 0.9);
        color: #2c3e50;
        padding: 1.25rem 1.5rem;
        border-radius: 20px 20px 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid rgba(255, 255, 255, 0.5);
        max-width: 85%;
    }
    
    /* Avatars */
    .user-avatar, .ai-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .user-avatar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
    .ai-avatar { background: white; color: #333; }
    
    /* Message Layout */
    .chat-message { margin: 1.5rem 0; display: flex; flex-direction: column; }
    .user-message { align-items: flex-end; }
    .bot-message { align-items: flex-start; }
    
    .message-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e0; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #a0aec0; }
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
        # Handle both old and new message formats
        timestamp = message.get("timestamp", "Now")
        message_id = message.get("message_id", f"msg_{len(st.session_state.messages)}")
        display_message(message["role"], message["content"], timestamp, message_id)
    
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


