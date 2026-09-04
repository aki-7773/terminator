// ---------- DOM Elements ----------
const chatListEl = document.getElementById('chatList');
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');
const chatNameEl = document.getElementById('chatName');
const newChatBtn = document.getElementById('newChatBtn');
const deleteChatBtn = document.getElementById('deleteChatBtn');
const renameChatBtn = document.getElementById('renameChatBtn');
const statusText = document.getElementById('statusText');

// ---------- State ----------
let currentChatId = null;
let chatList = [];
let chatHistory = [];

// ---------- Fetch Helpers ----------
async function fetchChats() {
    try {
        const res = await fetch('/chats');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (e) {
        console.error('Fetch chats error:', e);
        return [];
    }
}

async function fetchChatHistory(chatId) {
    try {
        const res = await fetch(`/chat/${chatId}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (e) {
        console.error('Fetch history error:', e);
        return { history: [] };
    }
}

async function sendMessageToChat(chatId, message) {
    try {
        const res = await fetch(`/chat/${chatId}/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        if (!res.ok) {
            const text = await res.text();
            throw new Error(`Server error ${res.status}: ${text.substring(0, 100)}`);
        }
        return await res.json();
    } catch (e) {
        console.error('Send message error:', e);
        return { error: e.message };
    }
}

async function createNewChat(name) {
    try {
        const res = await fetch('/chat/new', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        });
        if (!res.ok) {
            const text = await res.text();
            throw new Error(`Server error ${res.status}: ${text.substring(0, 100)}`);
        }
        return await res.json();
    } catch (e) {
        console.error('Create chat error:', e);
        return { error: e.message };
    }
}

async function deleteChat(chatId) {
    try {
        const res = await fetch(`/chat/${chatId}/delete`, { method: 'DELETE' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (e) {
        console.error('Delete chat error:', e);
        return { error: e.message };
    }
}

async function renameChat(chatId, newName) {
    try {
        const res = await fetch(`/chat/${chatId}/rename`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: newName })
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (e) {
        console.error('Rename chat error:', e);
        return { error: e.message };
    }
}

// ---------- Render Functions ----------
function renderChatList(chats) {
    chatListEl.innerHTML = '';
    chats.forEach(chat => {
        const item = document.createElement('div');
        item.className = `chat-item${chat.id === currentChatId ? ' active' : ''}`;
        item.dataset.chatId = chat.id;
        item.innerHTML = `
            <div class="chat-name">
                <span>${chat.name}</span>
                <span class="chat-badge">${chat.id === currentChatId ? '●' : ''}</span>
            </div>
            <div class="chat-preview">${chat.preview || 'New chat'}</div>
        `;
        item.addEventListener('click', () => switchChat(chat.id));
        chatListEl.appendChild(item);
    });
    if (newChatBtn) {
        newChatBtn.disabled = chats.length >= 5;
    }
}

function renderMessages(history) {
    chatMessages.innerHTML = '';
    if (!history || history.length === 0) {
        const welcome = document.createElement('div');
        welcome.className = 'message ai-message';
        welcome.innerHTML = `
            <div class="message-content">
                <div class="message-header">
                    <span class="message-avatar">🤖</span>
                    <span class="message-sender">Terminator AI</span>
                </div>
                <div class="message-text">
                    Hello! I'm Terminator AI, the ultimate assistant. I can do math, draw, search the web, analyze data, and chat! 🚀
                    <br><br>
                    Try asking me something!
                </div>
            </div>
        `;
        chatMessages.appendChild(welcome);
        return;
    }

    history.forEach(entry => {
        const isUser = entry.startsWith('You:');
        const sender = isUser ? 'You' : 'Terminator AI';
        const avatar = isUser ? '👤' : '🤖';
        const messageClass = isUser ? 'user-message' : 'ai-message';
        const text = isUser ? entry.substring(4) : entry.substring(sender.length + 2);
        
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${messageClass}`;
        msgDiv.innerHTML = `
            <div class="message-content">
                <div class="message-header">
                    <span class="message-avatar">${avatar}</span>
                    <span class="message-sender">${sender}</span>
                </div>
                <div class="message-text">${formatMessage(text)}</div>
            </div>
        `;
        chatMessages.appendChild(msgDiv);
    });
    scrollToBottom();
}

function formatMessage(text) {
    let html = text;
    html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    html = html.replace(/`([^`]*)`/g, '<code>$1</code>');
    html = html.replace(/\n/g, '<br>');
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    return html;
}

function scrollToBottom() {
    const container = document.getElementById('chatContainer');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

// ---------- Chat Switching ----------
async function switchChat(chatId) {
    if (chatId === currentChatId) return;
    currentChatId = chatId;
    
    const chat = chatList.find(c => c.id === chatId);
    if (chat) {
        chatNameEl.textContent = chat.name;
    }
    
    const data = await fetchChatHistory(chatId);
    chatHistory = data.history || [];
    renderMessages(chatHistory);
    
    document.querySelectorAll('.chat-item').forEach(el => el.classList.remove('active'));
    document.querySelector(`.chat-item[data-chat-id="${chatId}"]`)?.classList.add('active');
    
    userInput.focus();
}

// ---------- Send Message ----------
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message || !currentChatId) return;

    // Add user message
    const userMsg = document.createElement('div');
    userMsg.className = 'message user-message';
    userMsg.innerHTML = `
        <div class="message-content">
            <div class="message-header">
                <span class="message-avatar">👤</span>
                <span class="message-sender">You</span>
            </div>
            <div class="message-text">${formatMessage(message)}</div>
        </div>
    `;
    chatMessages.appendChild(userMsg);
    userInput.value = '';
    scrollToBottom();

    // Show typing
    typingIndicator.style.display = 'flex';

    try {
        const data = await sendMessageToChat(currentChatId, message);
        typingIndicator.style.display = 'none';
        
        if (data.error) {
            const errMsg = document.createElement('div');
            errMsg.className = 'message ai-message';
            errMsg.innerHTML = `
                <div class="message-content">
                    <div class="message-header">
                        <span class="message-avatar">🤖</span>
                        <span class="message-sender">Terminator AI</span>
                    </div>
                    <div class="message-text">⚠️ Error: ${data.error}</div>
                </div>
            `;
            chatMessages.appendChild(errMsg);
            scrollToBottom();
        } else if (data.response) {
            chatHistory = data.history || [];
            renderMessages(chatHistory);
            refreshChatList();
        } else {
            const errMsg = document.createElement('div');
            errMsg.className = 'message ai-message';
            errMsg.innerHTML = `
                <div class="message-content">
                    <div class="message-header">
                        <span class="message-avatar">🤖</span>
                        <span class="message-sender">Terminator AI</span>
                    </div>
                    <div class="message-text">⚠️ No response from server.</div>
                </div>
            `;
            chatMessages.appendChild(errMsg);
            scrollToBottom();
        }
    } catch (e) {
        typingIndicator.style.display = 'none';
        const errMsg = document.createElement('div');
        errMsg.className = 'message ai-message';
        errMsg.innerHTML = `
            <div class="message-content">
                <div class="message-header">
                    <span class="message-avatar">🤖</span>
                    <span class="message-sender">Terminator AI</span>
                </div>
                <div class="message-text">⚠️ Connection error: ${e.message}</div>
            </div>
        `;
        chatMessages.appendChild(errMsg);
        scrollToBottom();
    }
}

// ---------- Quick Actions ----------
function quickSend(text) {
    userInput.value = text;
    sendMessage();
}

// ---------- Chat Management ----------
async function refreshChatList() {
    chatList = await fetchChats();
    renderChatList(chatList);
}

async function createNewChat() {
    const name = prompt('Enter chat name:', `Chat ${chatList.length + 1}`);
    if (name === null) return; // user cancelled
    
    const trimmedName = name.trim();
    if (!trimmedName) {
        alert('Chat name cannot be empty.');
        return;
    }
    
    const data = await createNewChat(trimmedName);
    if (data.error) {
        alert('Error: ' + data.error);
    } else if (data.id) {
        await refreshChatList();
        await switchChat(data.id);
    } else {
        alert('Failed to create chat');
    }
}

async function deleteCurrentChat() {
    if (!currentChatId) return;
    if (chatList.length <= 1) {
        alert('Cannot delete the last chat.');
        return;
    }
    if (!confirm(`Delete "${chatNameEl.textContent}"?`)) return;
    const result = await deleteChat(currentChatId);
    if (result.error) {
        alert('Error: ' + result.error);
    } else if (result.status === 'deleted') {
        await refreshChatList();
        if (chatList.length > 0) {
            await switchChat(chatList[0].id);
        }
    } else {
        alert('Failed to delete chat');
    }
}

async function renameCurrentChat() {
    if (!currentChatId) return;
    const newName = prompt('Enter new chat name:', chatNameEl.textContent);
    if (newName === null) return;
    const trimmed = newName.trim();
    if (!trimmed || trimmed === chatNameEl.textContent) return;
    const result = await renameChat(currentChatId, trimmed);
    if (result.error) {
        alert('Error: ' + result.error);
    } else if (result.name) {
        chatNameEl.textContent = result.name;
        await refreshChatList();
    } else {
        alert('Failed to rename chat');
    }
}

// ---------- Keyboard Shortcut ----------
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// ---------- Event Listeners ----------
sendButton.addEventListener('click', sendMessage);
newChatBtn.addEventListener('click', createNewChat);
deleteChatBtn.addEventListener('click', deleteCurrentChat);
renameChatBtn.addEventListener('click', renameCurrentChat);

// ---------- Initialization ----------
async function init() {
    console.log('Initializing Terminator AI...');
    chatList = await fetchChats();
    console.log('Chats loaded:', chatList);
    
    if (chatList.length === 0) {
        console.log('No chats found, creating default...');
        const newChat = await createNewChat('Chat 1');
        if (newChat.id) {
            chatList = await fetchChats();
        }
    }
    
    renderChatList(chatList);
    
    if (chatList.length > 0) {
        const first = chatList[0];
        currentChatId = first.id;
        chatNameEl.textContent = first.name;
        const data = await fetchChatHistory(first.id);
        chatHistory = data.history || [];
        renderMessages(chatHistory);
        document.querySelector(`.chat-item[data-chat-id="${first.id}"]`)?.classList.add('active');
    }
    
    userInput.focus();
    console.log('Initialization complete!');
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
