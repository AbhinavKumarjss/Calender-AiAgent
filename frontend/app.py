import streamlit as st
import requests
import os
from dotenv import load_dotenv

##############################
##       DECLARATIONS       ##
############################## 

load_dotenv()
API_URL = os.getenv("API_URL")

##############################
##        FUNCTIONS         ##
############################## 

#Function To Fetch Data from Backend
def query_backend():
    print("Fetching Request ..")
    try:
        # Send the message list (just the content) to the backend
        message_list = [f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]
        response = requests.post(API_URL, json={"message": message_list})
        print("📡 Backend response:", response.text)
        return response.json().get("response", "⚠️ No response received.")
    except Exception as e:
        return f"❌ Error contacting backend"


##############################
##        STREAMLIT         ##
############################## 

st.title("🧠 AI Appointment Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Speak or type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = query_backend()

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
