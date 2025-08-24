import streamlit as st
import uuid
import streamlit.components.v1 as components
import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL, MAX_TOKENS, TEMPERATURE
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# ---------- Safety / API key ----------
if GOOGLE_API_KEY == "MISSING_API_KEY":
    st.error("""
    🚨 **API Key Missing!**
    
    MindSeek needs a Google Gemini API key to work.

    **Fix:**
    1) In Streamlit Cloud → App settings → Secrets/Env → add `GOOGLE_API_KEY`
    2) Value: key from Google AI Studio

    **Local dev:** create a `.env` with `GOOGLE_API_KEY=...`
    """)
    st.stop()

# ---------- Gemini config ----------
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
    model_name=GEMINI_MODEL,
    generation_config=genai.types.GenerationConfig(
        max_output_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
)

# ---------- Helpers ----------
def _copy_to_clipboard(text: str):
    """One‑click copy using a tiny invisible component (no HTML/JS in your layout)."""
    import base64
    b64 = base64.b64encode(text.encode("utf-8")).decode()
    components.html(
        f"""
        <script>
        const t = atob("{b64}");
        navigator.clipboard.writeText(t);
        </script>
        """,
        height=0,
    )

def process_message(prompt: str):
    if not prompt or not prompt.strip():
        return

    now = datetime.now(ZoneInfo("US/Pacific")).strftime("%H:%M")
    user_id = f"msg_{uuid.uuid4().hex}"
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": now,
        "message_id": user_id,
    })
    st.session_state.chat_count += 1

    try:
        with st.spinner("🤖 AI is thinking..."):
            response = model.generate_content(prompt)

            if response.text:
                resp_time = datetime.now().strftime("%H:%M")
                asst_id = f"msg_{uuid.uuid4().hex}"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.text,
                    "timestamp": resp_time,
                    "message_id": asst_id,
                })
                st.session_state.chat_count += 1
            else:
                st.error("Sorry, I couldn't generate a response. Try again.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.error("There was an error connecting to the AI service. Please check your API key and try again.")



def display_message(role, content, timestamp=None, message_id=None, idx=None):
    if timestamp is None:
        timestamp = "Now"
    if message_id is None:
        message_id = f"msg_{int(time.time()*1000)}_{idx or 0}"

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

    elif role == "assistant":
        # render the assistant bubble
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

        # assistant-only copy button (unique key)
        if st.button("📋 Copy", key=f"copy-{message_id}-btn"):
            _copy_to_clipboard(content)
            try:
                st.toast("Copied")
            except Exception:
                st.success("Copied")



def on_input_change():
    if st.session_state.get("chat_input"):
        prompt = st.session_state.chat_input.strip()
        if prompt:
            process_message(prompt)
            st.session_state["clear_input"] = True

# ---------- Page config ----------
st.set_page_config(
    page_title="MindSeek - AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Styles (CSS only) ----------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 1.6rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 0;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    @keyframes shimmer { 0% {transform: translateX(-100%);} 100% {transform: translateX(100%);} }
    .chat-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        min-height: 50px;
    }
    .chat-message { margin: 2rem 0; animation: fadeInUp 0.6s ease-out; position: relative; }
    .chat-message:not(:last-child)::after {
        content: ''; position: absolute; bottom: -1rem; left: 50%;
        transform: translateX(-50%); width: 80%; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
    }
    @keyframes fadeInUp { from {opacity:0; transform: translateY(30px);} to {opacity:1; transform: translateY(0);} }
    .message-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; padding: 0.5rem 0; }
    .user-avatar, .ai-avatar {
        width: 40px; height: 40px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); flex-shrink: 0;
    }
    .user-avatar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
    .ai-avatar { background: linear-gradient(135deg, #00d4aa 0%, #0099cc 100%); color: white; }
    .message-info { display: flex; flex-direction: column; gap: 0.25rem; }
    .user-name, .ai-name { font-weight: 600; font-size: 14px; color: #2c3e50; }
    .message-time { font-size: 12px; color: #6c757d; font-weight: 500; }
    .user-message { display: flex; flex-direction: column; align-items: flex-end; margin-bottom: 1.5rem; }
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;
        padding: 1.25rem 1.5rem; border-radius: 25px 25px 5px 25px; max-width: 85%;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.25); position: relative; animation: slideInRight 0.5s ease-out;
        word-wrap: break-word; line-height: 1.6; font-size: 15px;
    }
    .user-bubble::before {
        content: ''; position: absolute; right: -8px; top: 20px; width: 0; height: 0;
        border-left: 10px solid #764ba2; border-top: 8px solid transparent; border-bottom: 8px solid transparent;
    }
    @keyframes slideInRight { from {opacity:0; transform: translateX(30px);} to {opacity:1; transform: translateX(0);} }
    .bot-message { display: flex; flex-direction: column; align-items: flex-start; margin-bottom: 1.5rem; }
    .bot-bubble {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); color: #2c3e50;
        padding: 1.25rem 1.5rem; border-radius: 25px 25px 25px 5px; max-width: 85%;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1); border: 1px solid rgba(0,0,0,0.05);
        position: relative; animation: slideInLeft 0.5s ease-out;
        word-wrap: break-word; line-height: 1.6; white-space: pre-wrap; font-size: 15px;
    }
    .bot-bubble::before {
        content: ''; position: absolute; left: -8px; top: 20px; width: 0; height: 0;
        border-right: 10px solid #ffffff; border-top: 8px solid transparent; border-bottom: 8px solid transparent;
    }
    @keyframes slideInLeft { from {opacity:0; transform: translateX(-30px);} to {opacity:1; transform: translateX(0);} }
    .message-actions { display:none; } /* turned off; Streamlit button is used instead */
    .chat-input-container {
        background: rgba(255,255,255,0.95); border-radius: 25px; padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15); border: 2px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(15px); margin-top: 2rem; position: relative; transition: all 0.3s ease;
    }
    .chat-input-container:hover { box-shadow: 0 12px 40px rgba(0,0,0,0.2); transform: translateY(-2px); }
    .chat-input-container:focus-within { border-color: #667eea; box-shadow: 0 0 0 4px rgba(102,126,234,0.1); }
    .input-wrapper { display:flex; align-items:center; gap:1rem; background:#f8f9fa; border-radius:20px; padding:0.5rem; border:2px solid transparent; transition: all 0.3s ease; }
    .input-wrapper:focus-within { background:white; border-color:#667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
    .stTextInput > div > div > input {
        border:none !important; background:transparent !important; border-radius:15px !important;
        padding:1rem 1.5rem !important; font-size:16px !important; font-weight:500 !important;
        color:#2c3e50 !important; box-shadow:none !important; outline:none !important;
    }
    .stTextInput > div > div > input:focus { box-shadow:none !important; outline:none !important; }
    .stTextInput > div > div > input::placeholder { color:#6c757d !important; font-weight:400 !important; }
    .send-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; border:none; border-radius:50%;
        width:45px; height:45px; display:flex; align-items:center; justify-content:center; cursor:pointer;
        transition: all 0.3s ease; box-shadow:0 4px 15px rgba(102,126,234,0.3); font-size:18px;
    }
    .send-button:hover { background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%); transform: scale(1.1); box-shadow:0 6px 20px rgba(102,126,234,0.4); }
    .send-button:active { transform: scale(0.95); }
    .action-button {
        background: rgba(102, 126, 234, 0.1); color:#667eea; border:none; border-radius:50%;
        width:40px; height:40px; display:flex; align-items:center; justify-content:center; cursor:pointer;
        transition: all 0.3s ease; font-size:16px;
    }
    .action-button:hover { background: rgba(102,126,234,0.2); transform: scale(1.05); }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; border:none; border-radius:20px;
        padding:0.75rem 2rem; font-weight:600; font-size:16px; transition: all 0.3s ease; box-shadow:0 4px 15px rgba(102,126,234,0.3);
    }
    .stButton > button:hover { background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%); transform: translateY(-2px); box-shadow:0 6px 20px rgba(102,126,234,0.4); }
    .stButton > button:active { transform: translateY(0); }
    .sidebar-content {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius:15px; padding:1.5rem; margin:1rem 0; box-shadow:0 4px 15px rgba(0,0,0,0.05);
    }
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; padding:1rem; border-radius:15px; text-align:center; margin:1rem 0; box-shadow:0 4px 15px rgba(102,126,234,0.3);
    }
    @media (max-width: 768px) {
        .user-bubble, .bot-bubble { max-width: 90%; }
        .main-header { padding: 1.5rem; }
        .chat-input-container { padding: 1rem; }
        .message-header { flex-direction: column; align-items: flex-start; gap: 0.5rem; }
    }
    .main .block-container { scrollbar-width: thin; scrollbar-color: #667eea #f1f1f1; }
    .main .block-container::-webkit-scrollbar { width: 8px; }
    .main .block-container::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
    .main .block-container::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; }
    .main .block-container::-webkit-scrollbar-thumb:hover { background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%); }
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #667eea; font-size: 2rem; margin: 0;">🤖 MindSeek</h1>
        <p style="color: #666; margin: 0;">AI Chat Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚀 AI Model")
    model_option = st.selectbox(
        "Choose Model:",
        ["gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("### 🎭 Creativity Level")
    temperature = st.slider(
        "Creativity Level:",
        min_value=0.0,
        max_value=1.0,
        value=TEMPERATURE,
        step=0.1,
        help="Lower = more focused, Higher = more creative",
        label_visibility="collapsed"
    )

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_count = 0
        st.rerun()

    st.markdown("### 📊 Chat Statistics")
    st.markdown(f"""
    <div class="stats-card">
        <h3 style="margin: 0; font-size: 1.5rem;">{st.session_state.chat_count}</h3>
        <p style="margin: 0; opacity: 0.9;">Total Messages</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**Current Model:** {model_option}")
    st.markdown("### ℹ️ About")
    st.markdown("**Powered by Google Gemini AI**")
    st.markdown("**Built with ❤️ using Streamlit**")

# ---------- Header ----------
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 3rem; font-weight: 700;"> 🤖 MindSeek</h1>
    <p style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Your Intelligent AI Chat Assistant</p>
    <p style="margin: 0; font-size: 1rem; opacity: 0.8;">Powered by Google Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# ---------- Chat area ----------
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for i, message in enumerate(st.session_state.messages):
        timestamp = message.get("timestamp", "Now")
        message_id = message.get("message_id") or f"msg_{uuid.uuid4().hex}"
        display_message(message["role"], message["content"], timestamp, message_id, idx=i)



    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("clear_input"):
        st.session_state.chat_input = ""
        st.session_state["clear_input"] = False

    # input row
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([4, 1, 1])

    with col1:
        prompt = st.text_input(
            "Ask me anything...",
            key="chat_input",
            placeholder="Type your message here... (Press Enter to send)",
            label_visibility="collapsed",
            on_change=on_input_change
        )

    with col2:
        if st.button("📎", key="file_button", help="Attach file (coming soon)"):
            st.info("📎 File attachment feature coming in the next update!")

    with col3:
        if st.button("▶️", key="send_button", help="Send message"):
            if prompt and prompt.strip():
                process_message(prompt)
                st.session_state["clear_input"] = True
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin-top: 2rem;'>
    <p style="margin: 0; font-size: 1.1rem; font-weight: 600;">🤖 MindSeek - Powered by Google Gemini AI</p>
    <p style="margin: 0.5rem 0; opacity: 0.8;">Built with ❤️ using Streamlit</p>
    <p style="margin: 0; font-size: 0.9rem; opacity: 0.7;">Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</div>
""", unsafe_allow_html=True)
