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
API_KEY ="sk-5c1c04b7ab514115886ffd14a04ca39a"

headers = {"Authorization": f"Bearer {API_KEY}"}  # Use Bearer if required

# Function to get chatbot response
def get_chatbot_response(user_input):
    url = "https://api.deepseek.com/chat"  # Replace with the correct API endpoint
    payload = {'message': user_input}
    headers = {"Authorization": f"Bearer {API_KEY}"}  # Use Bearer token if required
    
    response = requests.post(url, json=payload, headers=headers)
    print("api is loaded")
    if response.status_code == 200:
        response_data = response.json()
        chatbot_response = response_data.get("response")  # Extract the chatbot reply
        return chatbot_response  # Return response instead of printing
    else:
        return f"Error: {response.status_code} - {response.text}"  # Return error details

# Streamlit UI
st.title("Mindseek Chatbot")
st.write("""Welcome! 
         Start chatting with the chatbot.""")

# User input
user_input = st.text_input("You: ", "")
print(f"user input: {user_input}")

if user_input:
    chatbot_response = get_chatbot_response(user_input)
    print("Chat response recivied..")
    st.write(f"Chatbot: {chatbot_response}")
