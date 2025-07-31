import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="🎓 FutureMe AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    .user-message {
        background-color: #E3F2FD;
        margin-left: 2rem;
    }
    .bot-message {
        background-color: #F5F5F5;
        margin-right: 2rem;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

def call_backend(message: str) -> str:
    """Call the backend API to get a response"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json={"message": message},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()["reply"]
        else:
            return f"Sorry, I encountered an error (Status: {response.status_code}). Please try again!"
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to the backend. Make sure the FastAPI server is running on http://localhost:8000"
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. Please try again!"
    except Exception as e:
        return f"❌ An unexpected error occurred: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">🎓 FutureMe AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2em;">Your AI companion for discovering the perfect college major</p>', unsafe_allow_html=True)
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Hi there! 👋 I'm FutureMe AI, and I'm here to help you discover which college major might be perfect for you! \n\nTell me about yourself - what are your interests, hobbies, or subjects you enjoy? What kind of activities make you feel excited and engaged?"
            }
        ]
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message"><strong>🤖 FutureMe AI:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    # Create columns for better layout
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your message here...",
            placeholder="e.g., I love solving puzzles and working with computers",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send 📤", use_container_width=True)
    
    # Handle user input
    if send_button and user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get response from backend
        with st.spinner("🤔 Thinking..."):
            bot_response = call_backend(user_input)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Rerun to update the chat display
        st.rerun()
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("### 📚 About FutureMe AI")
        st.markdown("""
        This AI chatbot helps high school students explore different college majors based on their interests, skills, and preferences.
        
        **How it works:**
        1. Share your interests and hobbies
        2. Get personalized major recommendations
        3. Learn about career paths and skills needed
        
        **Tips for better results:**
        - Be specific about what you enjoy
        - Mention subjects you excel in
        - Share your career aspirations
        """)
        
        st.markdown("---")
        st.markdown("### 🔧 System Status")
        
        # Test backend connection
        try:
            test_response = requests.get(f"{BACKEND_URL}/", timeout=5)
            if test_response.status_code == 200:
                st.success("✅ Backend Connected")
            else:
                st.error("❌ Backend Error")
        except:
            st.error("❌ Backend Offline")
        
        if st.button("Clear Chat History"):
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "Hi there! 👋 I'm FutureMe AI, and I'm here to help you discover which college major might be perfect for you! \n\nTell me about yourself - what are your interests, hobbies, or subjects you enjoy?"
                }
            ]
            st.rerun()

if __name__ == "__main__":
    main()