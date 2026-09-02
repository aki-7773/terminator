// ---------- State ----------
let currentChatId = null;
let chatList = [];
let chatHistory = [];

// DOM Elements
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

// ---------- Fetch Helpers ----------
async function fetchChats() {
    const res = await fetch('/chats');
    return res.json();
}

async function fetchChatHistory(chatId) {
    const res = await fetch(`/chat/${chatId}`);
    return res.json();
}

async function sendMessageToChat(chatId, message) {
    const res = await fetch(`/chat/${chatId}/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });
    return res.json();
}

async function createNewChat(name) {
    const res = await fetch('/chat/new', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });
    return res.json();
}

async function deleteChat(chatId) {
    const res = await fetch(`/chat/${chatId}/delete`, { method: 'DELETE' });
    return res.json();
}

async function renameChat(chatId, newName) {
    const res = await fetch(`/chat/${chatId}/rename`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newName })
    });
    return res.json();
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
    // Update new chat button
    newChatBtn.disabled = chats.length >= 5;
}

function renderMessages(history) {
    chatMessages.innerHTML = '';
    if (!history || history.length === 0) {
        // Show welcome message
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
                    Try asking me something or type <strong>help</strong> to see what I can do!
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
    // Basic formatting
    let html = text;
    html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    html = html.replace(/`([^`]*)`/g, '<code>$1</code>');
    html = html.replace(/\n/g, '<br>');
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    return html;
}

function scrollToBottom() {
    const container = document.getElementById('chatContainer');
    container.scrollTop = container.scrollHeight;
}

// ---------- Chat Switching ----------
async function switchChat(chatId) {
    if (chatId === currentChatId) return;
    // Save current chat state if needed (already saved on server)
    currentChatId = chatId;
    // Update UI
    const chat = chatList.find(c => c.id === chatId);
    if (chat) {
        chatNameEl.textContent = chat.name;
    }
    // Load history
    const data = await fetchChatHistory(chatId);
    chatHistory = data.history || [];
    renderMessages(chatHistory);
    // Highlight sidebar item
    document.querySelectorAll('.chat-item').forEach(el => el.classList.remove('active'));
    document.querySelector(`.chat-item[data-chat-id="${chatId}"]`)?.classList.add('active');
    // Focus input
    userInput.focus();
}

// ---------- Send Message ----------
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message || !currentChatId) return;

    // Add user message to UI immediately
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
    showTyping(true);

    try {
        const data = await sendMessageToChat(currentChatId, message);
        showTyping(false);
        if (data.response) {
            // Update history and render
            chatHistory = data.history || [];
            renderMessages(chatHistory);
            // Update chat list previews
            await refreshChatList();
        } else {
            // Error
            const errMsg = document.createElement('div');
            errMsg.className = 'message ai-message';
            errMsg.innerHTML = `
                <div class="message-content">
                    <div class="message-header">
                        <span class="message-avatar">🤖</span>
                        <span class="message-sender">Terminator AI</span>
                    </div>
                    <div class="message-text">Error: ${data.error || 'Something went wrong'}</div>
                </div>
            `;
            chatMessages.appendChild(errMsg);
            scrollToBottom();
        }
    } catch (e) {
        showTyping(false);
        const errMsg = document.createElement('div');
        errMsg.className = 'message ai-message';
        errMsg.innerHTML = `
            <div class="message-content">
                <div class="message-header">
                    <span class="message-avatar">🤖</span>
                    <span class="message-sender">Terminator AI</span>
                </div>
                <div class="message-text">Connection error: ${e.message}</div>
            </div>
        `;
        chatMessages.appendChild(errMsg);
        scrollToBottom();
    }
}

function showTyping(show) {
    typingIndicator.style.display = show ? 'flex' : 'none';
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
    // If current chat not in list (deleted), switch to first
    if (currentChatId && !chatList.find(c => c.id === currentChatId)) {
        if (chatList.length > 0) {
            await switchChat(chatList[0].id);
        } else {
            // Should not happen
        }
    }
}

async function createNewChat() {
    const name = prompt('Enter chat name:', `Chat ${chatList.length + 1}`);
    if (!name) return;
    const data = await createNewChat(name);
    if (data.id) {
        await refreshChatList();
        await switchChat(data.id);
    } else {
        alert(data.error || 'Failed to create chat');
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
    if (result.status === 'deleted') {
        await refreshChatList();
        // Switch to first available chat
        if (chatList.length > 0) {
            await switchChat(chatList[0].id);
        }
    } else {
        alert(result.error || 'Failed to delete chat');
    }
}

async function renameCurrentChat() {
    if (!currentChatId) return;
    const newName = prompt('Enter new chat name:', chatNameEl.textContent);
    if (!newName || newName === chatNameEl.textContent) return;
    const result = await renameChat(currentChatId, newName);
    if (result.name) {
        chatNameEl.textContent = result.name;
        await refreshChatList();
    } else {
        alert(result.error || 'Failed to rename chat');
    }
}

// ---------- Keyboard shortcuts ----------
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// ---------- Init ----------
async function init() {
    // Load chats
    chatList = await fetchChats();
    if (chatList.length === 0) {
        // Create default
        await createNewChat('Chat 1');
        chatList = await fetchChats();
    }
    renderChatList(chatList);
    // Set first chat as active
    const first = chatList[0];
    if (first) {
        currentChatId = first.id;
        chatNameEl.textContent = first.name;
        const data = await fetchChatHistory(first.id);
        chatHistory = data.history || [];
        renderMessages(chatHistory);
        document.querySelector(`.chat-item[data-chat-id="${first.id}"]`)?.classList.add('active');
    }
    userInput.focus();

    // Event listeners
    newChatBtn.addEventListener('click', createNewChat);
    deleteChatBtn.addEventListener('click', deleteCurrentChat);
    renameChatBtn.addEventListener('click', renameCurrentChat);
    sendButton.addEventListener('click', sendMessage);

    // Check status periodically
    setInterval(async () => {
        try {
            const res = await fetch('/status');
            if (res.ok) {
                statusText.textContent = 'Online';
                document.querySelector('.status-indicator .dot').className = 'dot online';
            } else {
                statusText.textContent = 'Offline';
                document.querySelector('.status-indicator .dot').className = 'dot offline';
            }
        } catch {
            statusText.textContent = 'Offline';
            document.querySelector('.status-indicator .dot').className = 'dot offline';
        }
    }, 30000);
}

init();
        }
    }
}
