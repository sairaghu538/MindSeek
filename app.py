import streamlit as st
import requests
# import os
# from dotenv import load_dotenv

# Get API Key from environment variables
# load_dotenv()
# API_KEY = os.getenv("DEEPSEEK_API_KEY") # Fetch from environment

# if not API_KEY:
#     raise ValueError("API Key is missing! Set DEEPSEEK_API_KEY as an environment variable.")

# print(API_KEY)

# exit

# API Key
API_KEY = "Enter_your_API_KEY"  # Replace with your actual key

# Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Function to get chatbot response
def get_chatbot_response(user_input):
    url = "https://api.deepseek.com/v1/chat/completions"  # ✅ Corrected API URL

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        "stream": False
    }
    
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        chatbot_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        return chatbot_response
    else:
        return f"Error: {response.status_code} - {response.text}"  # Return error details

# Streamlit UI
st.title("Mindseek Chatbot")
st.write("Welcome! Start chatting with the chatbot.")

# User input
user_input = st.text_input("Ask Anything: ", "")

if user_input:
    chatbot_response = get_chatbot_response(user_input)
    st.write(f"Chatbot: {chatbot_response}")


