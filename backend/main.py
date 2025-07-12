from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
import uvicorn
import os
import json
import glob
from typing import List, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

# Load environment variables
load_dotenv('../.env')

app = FastAPI(title="African Companies Chat Assistant")

# Add session middleware for chat history
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-change-in-production")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class ChatHistoryItem(BaseModel):
    user_message: str
    ai_response: str
    timestamp: str

def load_company_knowledge_base():
    """Load all company JSON files as knowledge base"""
    knowledge_base = []
    
    # Load from the enhanced data directory
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    data_dir = os.path.abspath(data_dir)
    
    print(f"Looking for JSON files in: {data_dir}")
    
    if os.path.exists(data_dir):
        json_files = glob.glob(os.path.join(data_dir, '*.json'))
        print(f"Found JSON files: {json_files}")
        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    company_data = json.load(f)
                    knowledge_base.append(company_data)
                    print(f"Loaded: {company_data.get('company_name', 'Unknown')}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    else:
        print(f"Data directory not found: {data_dir}")
    
    print(f"Loaded {len(knowledge_base)} companies into knowledge base")
    return knowledge_base

# Load company knowledge at startup
COMPANY_KNOWLEDGE = load_company_knowledge_base()

def get_ai_response(user_message: str, chat_history: List[Dict] = None) -> str:
    """Generate AI response using OpenAI and company knowledge with chat history"""
    try:
        # Setup OpenAI
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        
        # Create knowledge context
        knowledge_context = ""
        for company in COMPANY_KNOWLEDGE:
            knowledge_context += f"""
Company: {company.get('company_name', 'Unknown')}
Countries: {', '.join(company.get('countries', []))}
Sector: {company.get('sector', 'Unknown')}
Description: {company.get('business_description', 'No description available')}
Key People: {', '.join([f"{person.get('name', 'Unknown')} ({person.get('title', 'Unknown role')})" for person in company.get('key_people', [])])}
Transactions: {company.get('transactions', 'No transaction information available')}
---"""
        
        # Build chat history for context
        messages = [
            ("system", f"""You are a knowledgeable assistant specializing in African companies. 
            Use the following company information to answer questions:

{knowledge_context}

Guidelines:
- Answer questions based on the provided company data
- If asked about a company not in your knowledge base, politely mention that you don't have information about that specific company
- Be conversational and helpful
- Focus on African business insights when relevant
- If you don't have specific information, say so clearly
- Remember the conversation context and refer to previous messages when relevant
- Keep responses concise but informative""")
        ]
        
        # Add chat history to messages
        if chat_history:
            for item in chat_history[-10:]:  # Keep last 10 exchanges for context
                messages.append(("human", item.get("user_message", "")))
                messages.append(("assistant", item.get("ai_response", "")))
        
        # Add current message
        messages.append(("human", user_message))
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages(messages)
        
        # Generate response
        chain = prompt | llm
        response = chain.invoke({})
        
        return response.content
        
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "I apologize, but I'm having trouble processing your request right now. Please try again."

@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    """Serve the main chat interface"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: Request, message: ChatMessage):
    """Main chat endpoint with session-based chat history"""
    try:
        # Get or initialize chat history from session
        if "chat_history" not in request.session:
            request.session["chat_history"] = []
        
        chat_history = request.session["chat_history"]
        
        # Generate AI response with chat history context
        ai_response = get_ai_response(message.message, chat_history)
        
        # Add this exchange to chat history
        chat_item = {
            "user_message": message.message,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat()
        }
        
        chat_history.append(chat_item)
        
        # Keep only last 20 exchanges to prevent session from getting too large
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]
        
        request.session["chat_history"] = chat_history
        
        return ChatResponse(response=ai_response)
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/clear-history")
async def clear_chat_history(request: Request):
    """Clear chat history for the current session"""
    request.session["chat_history"] = []
    return {"message": "Chat history cleared"}

@app.get("/chat-history")
async def get_chat_history(request: Request):
    """Get current chat history"""
    chat_history = request.session.get("chat_history", [])
    return {"history": chat_history, "count": len(chat_history)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "companies_loaded": len(COMPANY_KNOWLEDGE)}

@app.get("/debug")
async def debug_info():
    """Debug endpoint to check loaded data"""
    return {
        "companies_loaded": len(COMPANY_KNOWLEDGE),
        "companies": [company.get('company_name', 'Unknown') for company in COMPANY_KNOWLEDGE]
    }

@app.post("/test-chat")
async def test_chat():
    """Simple test endpoint"""
    return {"response": "Test response - API is working!"}

@app.get("/test", response_class=HTMLResponse)
async def get_test_page(request: Request):
    """Serve test page"""
    return templates.TemplateResponse("test.html", {"request": request})

@app.get("/debug-page", response_class=HTMLResponse)
async def get_debug_page(request: Request):
    """Serve debug page"""
    return templates.TemplateResponse("debug.html", {"request": request})

@app.get("/simple", response_class=HTMLResponse)
async def get_simple_chat(request: Request):
    """Serve simple chat page"""
    return templates.TemplateResponse("simple.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
