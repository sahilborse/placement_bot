import streamlit as st
import requests
import time
import urllib.parse
import re

# Page config
st.set_page_config(page_title="Pre-Placement Chatbot", layout="wide")

# CSS styling and animated background
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(-45deg, #ff00ff, #ff5500, #5500ff, #00ffaa);
            background-size: 300% 300%;
            animation: animateBg 10s infinite alternate ease-in-out;
            z-index: -1;
        }
        @keyframes animateBg {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .chat-box {
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 10px;
            box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.1);
        }
    </style>
    <div class='background'></div>
""", unsafe_allow_html=True)

st.title("💬 Pre-Placement Chatbot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Format response
def format_guidance_text(guidance):
    formatted = re.sub(r"(\d+\.\s\*\*)(.*?)\*\*", r"<b>\1\2</b>", guidance)
    formatted = formatted.replace("\n", "<br>")
    return formatted

# User input
user_input = st.text_input("Ask your pre-placement question:", "", key="input")

# Submit
if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append(("You", user_input))

        with st.spinner("Thinking..."):
            try:
                encoded_input = urllib.parse.quote(user_input)
                api_url = f"http://127.0.0.1:8000/ai-guidance?question={user_input}"

                response = requests.get(api_url)
                if response.status_code == 200:
                    raw_guidance = response.json().get("guidance", "No guidance provided.")
                    formatted_guidance = format_guidance_text(raw_guidance)
                else:
                    formatted_guidance = f"❌ Server Error: {response.status_code}"

                time.sleep(1)
                st.session_state.chat_history.append(("Bot", formatted_guidance))

            except Exception as e:
                st.session_state.chat_history.append(("Bot", f"Error: {str(e)}"))

# Chat history display
for sender, message in st.session_state.chat_history:
    with st.container():
        if sender == "Bot":
            st.markdown(f"""
                <div class='chat-box'>
                    <h4>🤖 <b>{sender}</b></h4>
                    <p style='font-size: 16px; line-height: 1.6;'>{message}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='chat-box'>
                    <h4>🧑 <b>{sender}</b></h4>
                    <p style='font-size: 16px; line-height: 1.6;'>{message}</p>
                </div>
            """, unsafe_allow_html=True)

# Hide Streamlit footer and menu
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
