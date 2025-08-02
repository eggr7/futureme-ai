import streamlit as st
import requests
import os
import base64
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image 

def logo_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    return b64

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

# Custom CSS for better styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin: 1rem;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        color: #ffffff;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 300;
        margin-bottom: 2rem;
        line-height: 1.6;
        text-shadow: 0 1px 4px rgba(0,0,0,0.2);
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        border-radius: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.3s ease-in;
        position: relative;
    }
    
    .user-message {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        margin-left: 3rem;
        margin-right: 1rem;
    }
    
    .user-message::before {
        content: '👤';
        position: absolute;
        left: -2.5rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        background: white;
        border-radius: 50%;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        color: #1f2937;
        margin-right: 3rem;
        margin-left: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .bot-message::before {
        content: '🤖';
        position: absolute;
        right: -2.5rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50%;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 25px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        color: #1f2937 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1), 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        outline: none !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
        text-transform: none !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        margin: 1rem;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        font-weight: 500;
        text-align: center;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .status-error {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        font-weight: 500;
        text-align: center;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .thinking {
        animation: pulse 1.5s infinite;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .user-message, .bot-message {
            margin-left: 0.5rem;
            margin-right: 0.5rem;
        }
        
        .user-message::before, .bot-message::before {
            display: none;
        }
        
        .main-header {
            font-size: 2rem;
        }
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8, #6b46c1);
    }
</style>
""", unsafe_allow_html=True)

# Embed the image via relative HTML
st.markdown(
    """
    <div style="text-align: center;">
        <img src="assets/logoFMAI.png" width="180">
    </div>
    """,
    unsafe_allow_html=True
)

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

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Hi there! 👋 I'm FutureMe AI. Tell me about your interests, hobbies, or subjects you enjoy!"
        }]
    if "input_buffer" not in st.session_state:
        st.session_state.input_buffer = ""

    # Display chat messages
    for message in st.session_state.messages:
        css_class = "user-message" if message["role"] == "user" else "bot-message"
        label = "You:" if message["role"] == "user" else "🤖 FutureMe AI:"
        st.markdown(f'<div class="chat-message {css_class}"><strong>{label}</strong> {message["content"]}</div>', unsafe_allow_html=True)

    st.markdown("---")  # separator

    # Chat input at the bottom
    st.markdown(
        """
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

    # Process submission
    if submitted and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})

        with st.spinner("🤔 Thinking..."):
            st.markdown('<div class="thinking">🤖 FutureMe AI is analyzing your interests...</div>', unsafe_allow_html=True)
            bot_response = call_backend(user_input.strip())

        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown("### 📚 About FutureMe AI")
        st.markdown("""
        This AI chatbot helps students explore college majors based on their interests.
        - 🎯 Share your hobbies and strengths  
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
