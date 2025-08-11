// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const fabBtn = document.getElementById('fabBtn');
const minimizeBtn = document.getElementById('minimizeBtn');
const closeBtn = document.getElementById('closeBtn');
const quickActionBtns = document.querySelectorAll('.quick-action-btn');

// Session Management
let sessionId = generateSessionId();
let isTyping = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    focusInput();
});

// Generate unique session ID
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Initialize event listeners
function initializeEventListeners() {
    // Send message on button click
    sendBtn.addEventListener('click', sendMessage);
    
    // Send message on Enter key
    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
    
    // Input focus and typing indicators
    messageInput.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });
    
    messageInput.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
    });
    
    // Quick action buttons
    quickActionBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.dataset.action;
            handleQuickAction(action);
        });
    });
    
    // Control buttons
    minimizeBtn.addEventListener('click', minimizeChat);
    closeBtn.addEventListener('click', closeChat);
    fabBtn.addEventListener('click', toggleChat);
    
    // Auto-resize input
    messageInput.addEventListener('input', autoResizeInput);
}

// Send message function
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isTyping) return;
    
    // Add user message to chat
    addMessage('user', message);
    messageInput.value = '';
    autoResizeInput();
    
    // Show typing indicator for AI response
    addTypingIndicator();
    isTyping = true;
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                message: message,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Add AI response to chat
            addMessage('ai', data.message);
        } else {
            throw new Error(data.message || 'Failed to send message');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('ai', 'Sorry, I encountered an error. Please try again.');
    } finally {
        isTyping = false;
        focusInput();
    }
}

// Add message to chat
function addMessage(sender, content) {
    // Remove typing indicator if it exists
    removeTypingIndicator();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message slide-up`;
    
    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-${sender === 'ai' ? 'robot' : 'user'}"></i>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                <p>${formatMessage(content)}</p>
            </div>
            <div class="message-time">${currentTime}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Format message content (handle links, code blocks, etc.)
function formatMessage(content) {
    // Convert URLs to clickable links
    content = content.replace(
        /(https?:\/\/[^\s]+)/g, 
        '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );
    
    // Convert line breaks to <br> tags
    content = content.replace(/\n/g, '<br>');
    
    return content;
}

// Add typing indicator
function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai-message typing-indicator';
    typingDiv.id = 'typing-indicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Handle quick actions
function handleQuickAction(action) {
    let message = '';
    
    switch (action) {
        case 'start-design':
            message = "I'd like to start designing a custom sign. Can you help me with the process?";
            break;
        case 'get-quote':
            message = "I'm interested in getting a quote for a custom sign. What information do you need?";
            break;
        case 'view-portfolio':
            message = "Can you show me some examples of your previous work or portfolio?";
            break;
        default:
            return;
    }
    
    // Set the message in input and send it
    messageInput.value = message;
    sendMessage();
}



// Scroll to bottom of chat
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Focus on input
function focusInput() {
    messageInput.focus();
}

// Auto-resize input
function autoResizeInput() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

// Minimize chat
function minimizeChat() {
    const chatContainer = document.querySelector('.chat-container');
    chatContainer.classList.toggle('minimized');
    
    if (chatContainer.classList.contains('minimized')) {
        minimizeBtn.innerHTML = '<i class="fas fa-expand"></i>';
    } else {
        minimizeBtn.innerHTML = '<i class="fas fa-minus"></i>';
    }
}

// Close chat
function closeChat() {
    const chatContainer = document.querySelector('.chat-container');
    chatContainer.classList.add('hidden');
    
    // Show FAB
    fabBtn.style.display = 'flex';
}

// Toggle chat visibility
function toggleChat() {
    const chatContainer = document.querySelector('.chat-container');
    chatContainer.classList.remove('hidden');
    chatContainer.classList.remove('minimized');
    
    // Hide FAB
    fabBtn.style.display = 'none';
    
    // Focus on input
    focusInput();
}

// Utility function to debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add CSS for typing indicator
const typingStyles = `
    .typing-indicator .message-bubble {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
    }
    
    .typing-dots {
        display: flex;
        gap: 4px;
        align-items: center;
        padding: 8px 0;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        background: var(--text-light);
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dots span:nth-child(1) {
        animation-delay: -0.32s;
    }
    
    .typing-dots span:nth-child(2) {
        animation-delay: -0.16s;
    }
    
    @keyframes typing {
        0%, 80%, 100% {
            transform: scale(0.8);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    .chat-container.minimized {
        position: fixed;
        bottom: 0;
        right: 0;
        width: 400px;
        transform: none;
        z-index: 1000;
    }
    
    .chat-container.minimized .chat-messages,
    .chat-container.minimized .chat-input-container {
        display: none;
    }
    
    .chat-container.minimized .chat-header {
        border-radius: var(--border-radius-lg);
    }
    
    @media (max-width: 768px) {
        .chat-container.minimized {
            width: 100%;
            right: 0;
        }
    }
    
    .fab {
        display: none;
    }
    
    .input-wrapper.focused {
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .message a {
        color: var(--primary-color);
        text-decoration: none;
        font-weight: 500;
    }
    
    .message a:hover {
        text-decoration: underline;
    }
    
    .user-message .message a {
        color: white;
        text-decoration: underline;
    }
`;

// Inject typing styles
const styleSheet = document.createElement('style');
styleSheet.textContent = typingStyles;
document.head.appendChild(styleSheet);

// Export functions for potential external use
window.SignNizeChat = {
    sendMessage,
    addMessage,
    handleQuickAction,
    toggleChat,
    minimizeChat,
    closeChat
};
