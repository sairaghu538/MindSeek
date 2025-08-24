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

# Validate configuration with better error message
if not GOOGLE_API_KEY:
    print("⚠️  WARNING: GOOGLE_API_KEY not found!")
    print("   Please add your API key in Streamlit Cloud:")
    print("   1. Go to your app settings")
    print("   2. Add environment variable: GOOGLE_API_KEY")
    print("   3. Value: Your Gemini API key")
    print("   Or add to .env file for local development")
    # Don't raise error, let the app show a user-friendly message
    GOOGLE_API_KEY = "MISSING_API_KEY"
