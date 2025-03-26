import streamlit as st
import requests  # Or any other method to access DeepSeek


# Get the API key from environment variables
# api_key =os.getenv('DEEPSEEK_API_KEY')


def get_chatbot_response(user_input):
    url = "https://api.deepseek.com/chat"  # Replace with actual DeepSeek endpoint
    payload = {'message': user_input}
    headers = {"Authorization": "sk-5c1c04b7ab514115886ffd14a04ca39a"}
    response = requests.post(url, json=payload, headers= headers)
    if response.status_code == 200:
        print(response.json()) # check if the response is as expected
    else:
        print(f"Error: {response.status_code}")
    

# Streamlit App
st.title("Mindseek Chatbot")
st.write("Welcome! Start chatting with the chatbot.")

# User input
user_input = st.text_input("You: ", "")

if user_input:
    chatbot_response = get_chatbot_response(user_input)
    st.write(f"Chatbot: {chatbot_response}")