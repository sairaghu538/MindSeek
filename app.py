import streamlit as st
from google.cloud import dialogflow_v2 as dialogflow
import os
from google.oauth2 import service_account

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account_key.json"  # Replace with your path

# Dialogflow session ID (can be any unique string)
SESSION_ID = "AIzaSyB4_3gz6jDF8t75Cwhsc23fQNV8vQ64GsM"

# Initialize Dialogflow client
def get_dialogflow_response(user_input):
    project_id = "your-project-id"  # Replace with your Google Cloud project ID
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, SESSION_ID)

    # Create the text input for the query
    text_input = dialogflow.TextInput(text=user_input, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    # Get the response from Dialogflow
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})

    # Extract the response text
    chatbot_response = response.query_result.fulfillment_text
    return chatbot_response

# Streamlit UI
st.title("Google Gemini Chatbot (Dialogflow Example)")
st.write("Welcome! Start chatting with the chatbot.")

# User input
user_input = st.text_input("You: ", "")

if user_input:
    chatbot_response = get_dialogflow_response(user_input)
    st.write(f"Chatbot: {chatbot_response}")
