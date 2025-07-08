# 🚀 Quick Installation Guide

## Prerequisites
- Python 3.8+ installed
- OpenAI API key

## 📥 Installation Steps

### 1. Clone or Download Project
```bash
# If using git:
git clone <repository-url>
cd Akania-test

# Or extract downloaded ZIP file
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
# Copy example environment file
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux

# Edit .env file and add your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Start the Application
```bash
# Option 1: Enhanced startup script (recommended)
python start_server.py

# Option 2: Windows batch file
start_server.bat

# Option 3: Manual start
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Access the Chat Interface
Open your browser and go to: **http://localhost:8000**

---

## 🎯 What You'll Get

### Chat Interface
- Modern, responsive design
- Real-time chat with AI
- Session-based memory
- Knowledge about African companies

### Available Pages
- **Main Chat**: http://localhost:8000
- **Debug Page**: http://localhost:8000/debug
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🏢 Sample Questions to Try

- "Tell me about Sylndr"
- "What companies are in the database?"
- "Which African companies work in e-commerce?"
- "Give me details about the eyewear company"
- "What do you know about Egyptian startups?"

---

## 🔧 Troubleshooting

### Common Issues

**Error: uvicorn not found**
```bash
pip install uvicorn
```

**Error: OpenAI API key missing**
- Make sure you have a `.env` file
- Check that `OPENAI_API_KEY` is set correctly

**Port already in use**
```bash
# Use a different port
python start_server.py --port 8001
```

**Virtual environment issues**
```bash
# Recreate virtual environment
rmdir /s .venv    # Windows
rm -rf .venv      # macOS/Linux

python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

---

## 📞 Need Help?

Check the documentation files:
- `README_RESTRUCTURED.md` - Detailed project overview
- `PROJECT_SUMMARY.md` - Feature summary
- `FINAL_STATUS.md` - Current project status

Happy chatting with African companies! 🌍
