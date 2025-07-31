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
    st.markdown('<p class="subtitle">Your AI companion for discovering the perfect college major</p>', unsafe_allow_html=True)
    
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
            st.markdown('<div class="thinking">🤖 FutureMe AI is analyzing your interests...</div>', unsafe_allow_html=True)
            bot_response = call_backend(user_input)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Rerun to update the chat display
        st.rerun()
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("### 📚 About FutureMe AI")
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        This AI chatbot helps high school students explore different college majors based on their interests, skills, and preferences.
        
        <strong>How it works:</strong><br>
        🎯 Share your interests and hobbies<br>
        🎓 Get personalized major recommendations<br>
        💼 Learn about career paths and skills needed
        
        <strong>Tips for better results:</strong><br>
        💡 Be specific about what you enjoy<br>
        📚 Mention subjects you excel in<br>
        🚀 Share your career aspirations
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🔧 System Status")
        
        # Test backend connection
        try:
            test_response = requests.get(f"{BACKEND_URL}/", timeout=5)
            if test_response.status_code == 200:
                st.markdown('<div class="status-success">✅ Backend Connected</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-error">❌ Backend Error</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="status-error">❌ Backend Offline</div>', unsafe_allow_html=True)
        
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