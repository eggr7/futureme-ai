import streamlit as st
import requests
import os
import base64
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="🎓 FutureMe AI",
    page_icon=" 🐼 ",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
def load_custom_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css("styles/styles.css")

# Load logo image as base64 (fallback if HTML <img> fails)
def logo_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    return b64

image_path = "assets/logoFMAI.png"

if os.path.exists(image_path):
    logo = Image.open(image_path)
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{logo_to_base64(logo)}" width="180">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Logo not found.")

# Backend call
def call_backend(message: str) -> str:
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json={"message": message},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "error":
                return f"⚠️ {data.get('response', 'An error occurred')}"
            return data.get("response", data.get("reply", "No response received"))
        else:
            return f"❌ Error (Status: {response.status_code}). Please try again!"
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to backend. Is FastAPI running?"
    except requests.exceptions.Timeout:
        return "⏱️ Timeout. Please try again!"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# Main function
def main():
    st.markdown('<h1 class="main-header">🎓 FutureMe AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI companion for discovering the perfect college major</p>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Hi there! 👋 I'm FutureMe AI. Tell me about your interests, hobbies, or subjects you enjoy!"
        }]
    if "input_buffer" not in st.session_state:
        st.session_state.input_buffer = ""

    for message in st.session_state.messages:
        css_class = "user-message" if message["role"] == "user" else "bot-message"
        
        emoji = "👤" if message["role"] == "user" else "🤖"
        emoji_html = f'<span style="font-size: 1.8rem;">{emoji}</span>'
        label = f"{emoji_html} You:" if message["role"] == "user" else f"{emoji_html} FutureMe AI:"
        st.markdown(f'<div class="chat-message {css_class}"><strong>{label}</strong> {message["content"]}</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
        <div style="display: flex; justify-content: center;">
            <div style="width: 600px;">
    """, unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            label="Type your message here...",
            placeholder="e.g., I love science and helping others",
            label_visibility="collapsed",
            key="user_input"
        )
        submitted = st.form_submit_button("Send 📤")

    st.markdown("</div></div>", unsafe_allow_html=True)

    if submitted and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})

        with st.spinner("🤔 Thinking..."):
            st.markdown('<div class="thinking">🤖 FutureMe AI is analyzing your interests...</div>', unsafe_allow_html=True)
            bot_response = call_backend(user_input.strip())

        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()

    with st.sidebar:
        st.markdown("### 📚 About FutureMe AI")
        st.markdown("""
        This AI chatbot helps students explore college majors based on their interests.
        - 🌟 Share your hobbies and strengths  
        - 🎓 Get career suggestions  
        - 💼 Learn about possible paths  
        """)
        st.markdown("---")
        st.markdown("### 🔧 System Status")
        try:
            r = requests.get(f"{BACKEND_URL}/", timeout=5)
            if r.status_code == 200:
                st.success("✅ Backend Connected")
            else:
                st.error("❌ Backend Error")
        except:
            st.error("❌ Backend Offline")

        if st.button("Clear Chat History"):
            st.session_state.messages = [{
                "role": "assistant",
                "content": "Hi there! 👋 I'm FutureMe AI. Tell me about your interests!"
            }]
            st.rerun()

if __name__ == "__main__":
    main()
