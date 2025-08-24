import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Gemini API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Streamlit Configuration
STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")

# Model Configuration
GEMINI_MODEL = "gemini-1.5-flash"  # You can change this to gemini-1.5-pro for more advanced features
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# Validate configuration
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required!")
