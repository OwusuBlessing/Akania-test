// Global variables
let chatMessages, chatInput, sendButton, clearButton, loading;

// Initialize elements when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    chatMessages = document.getElementById('chatMessages');
    chatInput = document.getElementById('chatInput');
    sendButton = document.getElementById('sendButton');
    clearButton = document.getElementById('clearButton');
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
        clearButton: !!clearButton,
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

function clearHistory() {
    console.log('Clearing chat history...');
    
    // Show confirmation
    if (!confirm('Are you sure you want to clear the chat history?')) {
        return;
    }
    
    fetch('/clear-history', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('History cleared:', data);
        
        // Clear the visual chat messages (keep only the welcome message)
        const welcomeMessage = chatMessages.querySelector('.message.bot');
        chatMessages.innerHTML = '';
        if (welcomeMessage) {
            chatMessages.appendChild(welcomeMessage);
        }
        
        addMessage('🔄 Chat history has been cleared. You can start a fresh conversation!', false);
    })
    .catch(error => {
        console.error('Failed to clear history:', error);
        addMessage('❌ Failed to clear chat history: ' + error.message, false);
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
