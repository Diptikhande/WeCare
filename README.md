# WeCare - AI-Powered Therapist Chatbot

An empathetic AI-powered therapist chatbot web application designed to provide mental health support through conversational AI. The application features a responsive React frontend with an ocean blue color palette and a Python backend powered by vector embeddings and machine learning.

![WeCare Banner](https://via.placeholder.com/800x200/1e40af/ffffff?text=WeCare+AI+Therapist)

## 🌟 Features

- **Interactive Chatbot Interface**: Human-like conversational AI that responds empathetically
- **Vector Database Integration**: Advanced retrieval system for contextually relevant responses
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Ocean Blue Color Palette**: Calming and professional design aesthetic
- **Real-time Chat**: Instant responses with typing indicators
- **Session Management**: Persistent chat sessions with history
- **Error Handling**: Robust error handling and user feedback
- **Scalable Architecture**: Containerized with Docker for easy deployment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  React Frontend │◄──►│ Python Backend  │◄──►│ Vector Database │
│                 │    │                 │    │   (ChromaDB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                        │                        │
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  User Interface │    │  GenAI + Flask  │    │ Sentence Trans. │
│  - Chat Window  │    │  - API Routes   │    │ - Embeddings    │
│  - Message I/O  │    │  - Session Mgmt │    │ - Similarity    │
│  - Responsive   │    │  - Error Handle │    │ - Retrieval     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker (optional)

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Diptikhande/WeCare.git
   cd WeCare
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Start the backend server**
   ```bash
   python app.py
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

## 📁 Project Structure

```
WeCare/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── chatbot.py          # Core chatbot logic
│   ├── data/                   # Vector database storage
│   ├── app.py                  # Flask application
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Backend container
├── frontend/
│   ├── public/
│   │   └── index.html          # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.js   # Main chat interface
│   │   │   ├── Header.js       # App header
│   │   │   ├── MessageList.js  # Message display
│   │   │   └── MessageInput.js # Message input
│   │   ├── utils/
│   │   │   └── api.js          # API utilities
│   │   ├── App.js              # Main app component
│   │   └── index.js            # App entry point
│   ├── package.json            # Node dependencies
│   └── Dockerfile              # Frontend container
├── docker-compose.yml          # Multi-container setup
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🔧 Configuration

### Backend Configuration

Create a `.env` file in the `backend/` directory:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True

# OpenAI Configuration (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Vector Database Configuration
CHROMA_DB_PATH=./data/chroma_db
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Server Configuration
HOST=0.0.0.0
PORT=5000
```

### Frontend Configuration

The frontend automatically connects to the backend. For custom backend URLs, set:

```env
REACT_APP_BACKEND_URL=http://your-backend-url:5000
```

## 🤖 AI Components

### Vector Database (ChromaDB)
- **Purpose**: Stores therapist knowledge and responses
- **Technology**: ChromaDB with persistent storage
- **Embedding Model**: all-MiniLM-L6-v2 for semantic similarity

### Response Generation
- **Method**: Vector similarity search + template responses
- **Fallback**: Default empathetic responses for unknown queries
- **Context**: Maintains conversation context within sessions

### Knowledge Base
The system includes pre-loaded therapist responses for:
- Anxiety and stress management
- Depression support
- Relationship counseling
- Work-life balance
- Self-esteem building
- Sleep and wellness
- Crisis intervention guidelines

## 🌐 API Endpoints

### Chat API
- `POST /api/chat` - Send message and get response
- `GET /api/chat/history/{session_id}` - Get chat history
- `POST /api/chat/reset/{session_id}` - Reset chat session

### Health Check
- `GET /api/health` - Check service status

### Example API Usage

```javascript
// Send a message
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "I'm feeling anxious today",
    session_id: "user123"
  })
});

const data = await response.json();
console.log(data.response); // Therapist response
```

## 🎨 Design System

### Color Palette (Ocean Blue)
- **Primary**: #1e40af (Blue 800)
- **Secondary**: #3730a3 (Indigo 800)
- **Accent**: #3b82f6 (Blue 500)
- **Background**: Linear gradients of blues
- **Text**: #1f2937 (Gray 800)

### Typography
- **Font**: System fonts (-apple-system, BlinkMacSystemFont, 'Segoe UI')
- **Headers**: 600 weight
- **Body**: 400 weight
- **Accent**: 500 weight

### Components
- **Glass-morphism**: Backdrop blur effects
- **Rounded corners**: 8px-20px border radius
- **Shadows**: Subtle drop shadows for depth
- **Animations**: Smooth transitions and hover effects

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Manual Testing
1. Start both frontend and backend
2. Open http://localhost:3000
3. Send test messages
4. Verify responses are appropriate and empathetic
5. Test session persistence and reset functionality

## 📈 Performance Optimization

### Backend
- **Caching**: Vector embeddings cached for faster retrieval
- **Async Processing**: Non-blocking response generation
- **Connection Pooling**: Efficient database connections

### Frontend
- **Code Splitting**: Lazy loading of components
- **Memoization**: React.memo for preventing unnecessary re-renders
- **Bundle Optimization**: Webpack optimizations in production

## 🔒 Security Considerations

- **Input Validation**: All user inputs are validated and sanitized
- **Rate Limiting**: API rate limiting to prevent abuse
- **Session Security**: Secure session management
- **CORS**: Proper CORS configuration
- **Environment Variables**: Sensitive data in environment variables

## 🚀 Deployment

### Production Docker Build
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment Options
- **AWS**: ECS/EKS with RDS
- **Google Cloud**: Cloud Run with Cloud SQL
- **Azure**: Container Instances with Cosmos DB
- **Heroku**: Direct deployment with add-ons

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- **Issues**: Open a GitHub issue
- **Email**: support@wecare.ai
- **Documentation**: Check the wiki for detailed guides

## 🙏 Acknowledgments

- **OpenAI**: For language model inspirations
- **ChromaDB**: For vector database technology
- **React**: For the frontend framework
- **Flask**: For the backend framework
- **Sentence Transformers**: For embedding models

## 📊 Mental Health Resources

If you're experiencing a mental health crisis, please reach out to professional services:

- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **NAMI**: National Alliance on Mental Illness - nami.org

Remember: This chatbot is for support and information only, not a replacement for professional mental health care.

---

Made with ❤️ and 🧠 by the WeCare Team