from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import json
import glob
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

app = FastAPI(title="African Companies Chat Assistant")

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

def load_company_knowledge_base():
    """Load all company JSON files as knowledge base"""
    knowledge_base = []
    data_dir = os.path.join(os.path.dirname(__file__), 'akania', 'src', 'data')
    
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
        print(f"Data directory does not exist: {data_dir}")
    
    return knowledge_base

# Load knowledge base on startup
COMPANY_KNOWLEDGE = load_company_knowledge_base()
print(f"Loaded {len(COMPANY_KNOWLEDGE)} companies into knowledge base")

def create_chat_prompt():
    """Create the chat prompt template"""
    return ChatPromptTemplate.from_messages([
        ("system", """
        You are an expert African business analyst and chatbot assistant. You have access to a comprehensive database of African companies with detailed information.

        **Your Knowledge Base Contains:**
        {knowledge_base}

        **Instructions:**
        - Answer questions about African companies using ONLY the information from your knowledge base
        - Be conversational, friendly, and helpful
        - If asked about a company not in your database, politely say you don't have information about that specific company
        - Provide specific details when available (countries, sectors, key people, business descriptions)
        - You can compare companies, provide insights, and answer general questions about African business trends based on your data
        - Keep responses concise but informative
        - Use emojis occasionally to make responses more engaging

        **Example responses:**
        - "Based on my data, Sylndr operates in Egypt and focuses on automotive e-commerce..."
        - "I have information on several companies across different sectors. Lapaire operates in 7 African countries..."
        - "Comparing the companies in my database, I see representation from Egypt, Kenya, Mozambique..."

        User Question: {user_message}
        """),
    ])

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """
    Chat endpoint that answers questions using the company knowledge base
    """
    try:
        user_message = message.message.strip()
        
        # Check if we have any companies loaded
        if not COMPANY_KNOWLEDGE:
            return ChatResponse(response="Sorry, no company data is currently loaded. Please check the server logs.")
        
        # Initialize LLM
        llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0.7)
        
        # Create prompt
        prompt = create_chat_prompt()
        
        # Format knowledge base for context
        knowledge_context = ""
        for i, company in enumerate(COMPANY_KNOWLEDGE, 1):
            knowledge_context += f"\n{i}. Company: {company.get('company_name', 'Unknown')}\n"
            knowledge_context += f"   Countries: {', '.join(company.get('countries', []))}\n"
            knowledge_context += f"   Sector: {', '.join(company.get('sector', []))}\n"
            knowledge_context += f"   Description: {company.get('business_description', 'N/A')}\n"
            knowledge_context += f"   Key People: {len(company.get('key_people', []))} people\n"
            knowledge_context += f"   Transactions: {company.get('transactions', 'N/A')}\n"
        
        # Create chain
        chain = prompt | llm
        
        # Get response
        response = chain.invoke({
            "knowledge_base": knowledge_context,
            "user_message": user_message
        })
        
        return ChatResponse(response=response.content)
            
    except Exception as e:
        print(f"Chat error: {e}")
        import traceback
        traceback.print_exc()
        return ChatResponse(response=f"Sorry, I encountered an error: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    """
    Serve the chat interface HTML page
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>African Companies Knowledge Bot</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            .chat-container {
                width: 90%;
                max-width: 900px;
                height: 90vh;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                text-align: center;
                font-size: 22px;
                font-weight: bold;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #f8f9fa;
                display: flex;
                flex-direction: column;
            }
            
            .message {
                margin-bottom: 20px;
                display: flex;
                max-width: 80%;
                animation: slideIn 0.3s ease-out;
            }
            
            .message.user {
                align-self: flex-end;
                justify-content: flex-end;
            }
            
            .message.bot {
                align-self: flex-start;
                justify-content: flex-start;
            }
            
            .message-content {
                padding: 15px 20px;
                border-radius: 20px;
                word-wrap: break-word;
                white-space: pre-wrap;
                line-height: 1.4;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .message.user .message-content {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-bottom-right-radius: 5px;
            }
            
            .message.bot .message-content {
                background: white;
                color: #333;
                border: 1px solid #e0e0e0;
                border-bottom-left-radius: 5px;
            }
            
            .chat-input-container {
                padding: 20px;
                background: white;
                border-top: 1px solid #e0e0e0;
                display: flex;
                gap: 15px;
                align-items: center;
            }
            
            .chat-input {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: all 0.3s ease;
                background: #f8f9fa;
            }
            
            .chat-input:focus {
                border-color: #667eea;
                background: white;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .send-button {
                padding: 15px 25px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                transition: all 0.3s ease;
                min-width: 80px;
            }
            
            .send-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            
            .send-button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 15px;
                color: #666;
                font-style: italic;
                background: #f0f8ff;
                margin: 10px 20px;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }
            
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .stats {
                background: #f0f8ff;
                padding: 10px 15px;
                margin: 10px 0;
                border-radius: 10px;
                border-left: 4px solid #667eea;
                font-size: 14px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                🌍 African Companies Knowledge Bot
                <div style="font-size: 14px; font-weight: normal; margin-top: 5px; opacity: 0.9;">
                    Ask me anything about African companies in my database
                </div>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message bot">
                    <div class="message-content">
                        👋 Welcome! I'm your African Companies Knowledge Assistant. 
                        
                        I have detailed information about several African companies including Sylndr, Lapaire, Merec Industries, SanLei, and MONISHOP.
                        
                        You can ask me:
                        • "Tell me about Sylndr"
                        • "Which companies operate in multiple countries?"
                        • "What sectors are represented?"
                        • "Compare Lapaire and Sylndr"
                        • Or any other question about these companies!
                    </div>
                </div>
            </div>
            
            <div class="loading" id="loading">
                🤔 Thinking...
            </div>
            
            <div class="chat-input-container">
                <input type="text" class="chat-input" id="chatInput" placeholder="Ask me about African companies..." onkeypress="handleKeyPress(event)">
                <button class="send-button" onclick="testAPI()" id="testButton" style="background: #28a745; margin-right: 10px;">Test</button>
                <button class="send-button" onclick="sendMessage()" id="sendButton">Send</button>
            </div>
        </div>

        <script>
            // Global variables
            let chatMessages, chatInput, sendButton, testButton, loading;
            
            // Initialize elements when DOM is loaded
            document.addEventListener('DOMContentLoaded', function() {
                chatMessages = document.getElementById('chatMessages');
                chatInput = document.getElementById('chatInput');
                sendButton = document.getElementById('sendButton');
                testButton = document.getElementById('testButton');
                loading = document.getElementById('loading');
                
                // Focus input
                if (chatInput) {
                    chatInput.focus();
                }
                
                console.log('Chat interface initialized successfully');
                console.log('Elements found:', {
                    chatMessages: !!chatMessages,
                    chatInput: !!chatInput,
                    sendButton: !!sendButton,
                    testButton: !!testButton,
                    loading: !!loading
                });
            });

            function addMessage(content, isUser = false) {
                console.log('Adding message:', content, 'isUser:', isUser);
                
                if (!chatMessages) {
                    console.error('chatMessages element not found!');
                    return;
                }
                
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
                
                const contentDiv = document.createElement('div');
                contentDiv.className = 'message-content';
                contentDiv.textContent = content;
                
                messageDiv.appendChild(contentDiv);
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                console.log('Message added successfully');
            }

            function testAPI() {
                console.log('Testing API...');
                addMessage('🔧 Testing API connection...', false);
                
                fetch('/test-chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => {
                    console.log('Test API response status:', response.status);
                    return response.json();
                })
                .then(data => {
                    console.log('Test API response data:', data);
                    addMessage('✅ ' + data.response, false);
                })
                .catch(error => {
                    console.error('API test failed:', error);
                    addMessage('❌ API connection failed: ' + error.message, false);
                });
            }

            function sendMessage() {
                if (!chatInput || !sendButton || !loading) {
                    console.error('Required elements not found!');
                    return;
                }
                
                const message = chatInput.value.trim();
                if (!message) {
                    console.log('Empty message, not sending');
                    return;
                }

                console.log('Sending message:', message);

                // Add user message (appears on the right)
                addMessage(message, true);
                
                // Clear input and disable button
                chatInput.value = '';
                sendButton.disabled = true;
                sendButton.textContent = 'Sending...';
                loading.style.display = 'block';

                // Make the API call
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                })
                .then(response => {
                    console.log('Chat API response status:', response.status);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Chat API response data:', data);
                    if (data.response) {
                        addMessage(data.response, false);
                    } else {
                        addMessage('Sorry, I received an empty response.', false);
                    }
                })
                .catch(error => {
                    console.error('Chat API request failed:', error);
                    addMessage('Sorry, I couldn\'t connect to the server. Error: ' + error.message, false);
                })
                .finally(() => {
                    // Re-enable button and hide loading
                    if (sendButton) {
                        sendButton.disabled = false;
                        sendButton.textContent = 'Send';
                    }
                    if (loading) {
                        loading.style.display = 'none';
                    }
                    if (chatInput) {
                        chatInput.focus();
                    }
                });
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    sendMessage();
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

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

@app.get("/test")
async def get_test_page():
    """Serve simple test page"""
    with open("test_chat.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/debug-page")
async def get_debug_page():
    """Serve debug page for chat interface testing"""
    with open("debug_chat.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/simple")
async def get_simple_chat():
    """Serve simple chat page for basic testing"""
    with open("simple_chat.html", "r") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
