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

# Page configuration
st.set_page_config(
    page_title="MindSeek - AI Chat Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #667eea;
    }
    .bot-message {
        background-color: #e8f4fd;
        border-left-color: #764ba2;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

# Sidebar
with st.sidebar:
    st.title("🧠 MindSeek Settings")
    
    # Model selection
    model_option = st.selectbox(
        "Choose Model:",
        ["gemini-1.5-flash", "gemini-1.5-pro"],
        index=0
    )
    
    # Temperature slider
    temperature = st.slider(
        "Creativity Level:",
        min_value=0.0,
        max_value=1.0,
        value=TEMPERATURE,
        step=0.1,
        help="Lower values = more focused, Higher values = more creative"
    )
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat_count = 0
        st.rerun()
    
    # Chat statistics
    st.markdown("---")
    st.markdown("**Chat Statistics:**")
    st.markdown(f"Total Messages: {st.session_state.chat_count}")
    st.markdown(f"Current Model: {model_option}")
    
    # About section
    st.markdown("---")
    st.markdown("**About MindSeek:**")
    st.markdown("Powered by Google Gemini AI")
    st.markdown("Built with Streamlit")

# Main header
st.markdown("""
<div class="main-header">
    <h1>🧠 MindSeek</h1>
    <p>Your Intelligent AI Chat Assistant</p>
</div>
""", unsafe_allow_html=True)

# Chat interface
chat_container = st.container()

with chat_container:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_count += 1
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                # Get response from Gemini
                response = model.generate_content(prompt)
                
                if response.text:
                    # Simulate typing effect
                    full_response = response.text
                    for i in range(0, len(full_response), 10):
                        message_placeholder.markdown(full_response[:i+10] + "▌")
                        time.sleep(0.01)
                    message_placeholder.markdown(full_response)
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    st.session_state.chat_count += 1
                else:
                    message_placeholder.error("Sorry, I couldn't generate a response. Please try again.")
                    
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                message_placeholder.error(error_msg)
                st.error("There was an error connecting to the AI service. Please check your API key and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🧠 MindSeek - Powered by Google Gemini AI | Built with ❤️ using Streamlit</p>
    <p>Last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)


