import os
from dotenv import load_dotenv
from google import genai

# Load env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print(f"API Key present: {bool(api_key)}")
if api_key:
    print(f"Key preview: {api_key[:5]}...")

try:
    client = genai.Client(api_key=api_key)
    print("Client initialized. Attempting to list models...")
    
    # List models
    print("Available models:")
    for m in client.models.list():
        print(f" - {m.name}")
        # Just check for gen 1.5 flash existence
        if "gemini-1.5-flash" in m.name:
            print("   (Found target model!)")
                
    print("\nAttempting generation with 'gemini-1.5-flash'...")
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Hello, this is a test.",
    )
    print(f"\nSUCCESS! Response: {response.text}")

except Exception as e:
    print(f"\nFAILED with validation script: {e}")
