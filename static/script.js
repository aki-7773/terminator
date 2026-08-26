// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');
const statusText = document.getElementById('statusText');
const statusDot = document.querySelector('.status-dot');

// Send message on Enter key
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Auto-resize input
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Quick send function
function quickSend(text) {
    userInput.value = text;
    sendMessage();
}

// Send message function
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    userInput.value = '';
    userInput.style.height = 'auto';
    
    // Show typing indicator
    showTyping(true);
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Hide typing indicator
        showTyping(false);
        
        if (data.status === 'success') {
            addMessage(data.response, 'ai');
        } else {
            addMessage(`Error: ${data.error || 'Something went wrong'}`, 'ai');
        }
        
    } catch (error) {
        showTyping(false);
        addMessage(`Connection error: ${error.message}`, 'ai');
    }
    
    // Scroll to bottom
    scrollToBottom();
}

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender === 'user' ? 'user-message' : 'ai-message'}`;
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const header = document.createElement('div');
    header.className = 'message-header';
    
    const avatar = document.createElement('span');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';
    
    const name = document.createElement('span');
    name.className = 'message-sender';
    name.textContent = sender === 'user' ? 'You' : 'Terminator AI';
    
    header.appendChild(avatar);
    header.appendChild(name);
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.innerHTML = formatMessage(text);
    
    content.appendChild(header);
    content.appendChild(textDiv);
    messageDiv.appendChild(content);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Format message (handle line breaks, code blocks, etc.)
function formatMessage(text) {
    // Handle code blocks
    text = text.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    
    // Handle inline code
    text = text.replace(/`([^`]*)`/g, '<code>$1</code>');
    
    // Handle line breaks
    text = text.replace(/\n/g, '<br>');
    
    // Handle bold
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    return text;
}

// Show/hide typing indicator
function showTyping(show) {
    typingIndicator.style.display = show ? 'flex' : 'none';
}

// Scroll to bottom of chat
function scrollToBottom() {
    const container = document.getElementById('chatContainer');
    container.scrollTop = container.scrollHeight;
}

// Check AI status
async function checkStatus() {
    try {
        const response = await fetch('/status');
        const data = await response.json();
        
        if (data.status === 'success') {
            statusText.textContent = 'Online';
            statusDot.style.background = '#00ff64';
        }
    } catch (error) {
        statusText.textContent = 'Offline';
        statusDot.style.background = '#ff4444';
    }
}

// Update status periodically
checkStatus();
setInterval(checkStatus, 30000);

// Focus input on load
userInput.focus();

// Handle reset (optional)
async function resetConversation() {
    if (confirm('Reset the conversation?')) {
        try {
            await fetch('/reset', { method: 'POST' });
            chatMessages.innerHTML = '';
            addMessage("✨ Conversation reset! Let's start fresh.", 'ai');
        } catch (error) {
            console.error('Reset failed:', error);
        }
    }
}
