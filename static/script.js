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

async function apiCreateNewChat(name) {
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
        console.error('Create chat API error:', e);
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
        addMessage("Hello! I'm Terminator AI, the ultimate assistant. I can do math, draw, search the web, analyze data, and chat! 🚀\n\nTry asking me something!", false, null);
        return;
    }

    history.forEach(entry => {
        const isUser = entry.startsWith('You:');
        const sender = isUser ? 'You' : 'Terminator AI';
        const text = isUser ? entry.substring(4) : entry.substring(sender.length + 2);
        addMessage(text, isUser, null);
    });
    scrollToBottom();
}

function addMessage(text, isUser, image) {
    // Ensure text is a string
    if (typeof text !== 'string') {
        text = JSON.stringify(text);
    }
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
    const avatar = isUser ? '👤' : '🤖';
    const sender = isUser ? 'You' : 'Terminator AI';
    let content = `
        <div class="message-content">
            <div class="message-header">
                <span class="message-avatar">${avatar}</span>
                <span class="message-sender">${sender}</span>
            </div>
            <div class="message-text">${formatMessage(text)}</div>
    `;
    if (image) {
        content += `<div style="margin-top:8px;"><img src="${image}" style="max-width:100%; border-radius:8px;"/></div>`;
    }
    content += `</div>`;
    msgDiv.innerHTML = content;
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
}

function formatMessage(text) {
    // Ensure text is string (just in case)
    if (typeof text !== 'string') text = String(text);
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
    addMessage(message, true, null);
    userInput.value = '';
    scrollToBottom();

    // Show typing
    typingIndicator.style.display = 'flex';

    try {
        const data = await sendMessageToChat(currentChatId, message);
        typingIndicator.style.display = 'none';
        
        console.log('📦 Server response:', data); // debug

        if (data.error) {
            addMessage('⚠️ Error: ' + data.error, false, null);
        } else {
            // Extract response text and image
            let responseText = data.response || data.text || data.message || '';
            let image = data.image || null;

            // If responseText is an object, stringify it
            if (typeof responseText === 'object') {
                responseText = JSON.stringify(responseText);
            }

            addMessage(responseText, false, image);
            refreshChatList();
        }
    } catch (e) {
        typingIndicator.style.display = 'none';
        addMessage('⚠️ Connection error: ' + e.message, false, null);
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
    console.log('✅ createNewChat() UI handler called!');
    const name = prompt('Enter chat name:', `Chat ${chatList.length + 1}`);
    if (name === null) {
        console.log('User cancelled');
        return;
    }
    
    const trimmedName = name.trim();
    if (!trimmedName) {
        alert('Chat name cannot be empty.');
        return;
    }
    
    console.log(`Creating new chat with name: "${trimmedName}"`);
    const data = await apiCreateNewChat(trimmedName);
    console.log('Server response:', data);
    if (data && data.error) {
        alert('Error: ' + data.error);
    } else if (data && data.id) {
        await refreshChatList();
        await switchChat(data.id);
    } else {
        alert('Failed to create chat. Server response was invalid.');
    }
}

window.createNewChat = createNewChat;

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
if (newChatBtn) {
    newChatBtn.addEventListener('click', createNewChat);
}
deleteChatBtn.addEventListener('click', deleteCurrentChat);
renameChatBtn.addEventListener('click', renameCurrentChat);

window.sendMessage = sendMessage;
window.quickSend = quickSend;

// ---------- Initialization ----------
async function init() {
    console.log('Initializing Terminator AI...');
    chatList = await fetchChats();
    console.log('Chats loaded:', chatList);
    
    if (chatList.length === 0) {
        console.log('No chats found, creating default...');
        const newChat = await apiCreateNewChat('Chat 1');
        if (newChat && newChat.id) {
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

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
