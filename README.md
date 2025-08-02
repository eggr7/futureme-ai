# 🎓 FutureMe AI

A conversational AI chatbot that helps high school students discover which college major to choose. Built with FastAPI backend and Streamlit frontend for a hackathon project.

## 🚀 Features

- **Interactive Chat Interface**: Clean and modern Streamlit UI
- **Smart Recommendations**: AI-powered major suggestions based on interests
- **Real-time Responses**: Fast FastAPI backend with RESTful API
- **Extensible Design**: Easy to integrate with OpenAI or other AI services
- **Static Data**: No database required - uses JSON for major information

## 🏗️ Project Structure

```
futureme-ai/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── api/
│   │   └── routes.py        # POST /chat endpoint
│   ├── core/
│   │   └── logic.py         # Chatbot logic
│   ├── data/
│   │   └── majors.json      # Static major data
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app.py              # Streamlit app
│   ├── requirements.txt
│   └── .env.example
├── README.md
└── .gitignore
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys if needed
```

4. Run the FastAPI server:
```bash
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up environment variables:
```bash
cp .env.example .env
# Edit .env if you need to change the backend URL
```

4. Run the Streamlit app:
```bash
streamlit run app.py
```

The frontend will be available at `http://localhost:8501`

## 🎯 Usage

1. Start both the backend and frontend servers (see setup instructions above)
2. Open your browser to `http://localhost:8501`
3. Start chatting with FutureMe AI about your interests and preferences
4. Get personalized college major recommendations!

## 🔧 API Endpoints

### POST /api/chat
Receives user messages and returns AI responses.

**Request:**
```json
{
  "message": "I love solving problems and working with computers"
}
```

**Response:**
```json
{
  "reply": "Based on your interest in technology, you might enjoy Computer Science! It involves problem-solving through code and building innovative solutions."
}
```

## 📊 Available Majors

The system currently includes information about:
- Computer Science
- Psychology  
- Business
- Fine Arts
- Biology

Each major includes:
- Description
- Required skills
- Career paths

## 🚀 Future Enhancements

- [ ] Integration with OpenAI GPT for more sophisticated responses
- [ ] User profile persistence
- [ ] More detailed major information and career paths
- [ ] Personality assessment integration
- [ ] Export chat history and recommendations
- [ ] Mobile-responsive design improvements

## 🤝 Contributing

This is a hackathon project, but contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🏆 Hackathon Notes

Built for PANDA Hacks 2025 with focus on:
- Clean, minimal design
- Fast development and deployment
- Extensible architecture for future AI integration
- User-friendly interface for high school students

---

**Happy coding! 🚀**