// 获取 DOM 元素
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const chatMessages = document.getElementById('chatMessages');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');

let isWaiting = false;

// 添加消息到聊天区域
function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    
    if (type === 'ai') {
        const img = document.createElement('img');
        img.src = '/static/img/yui_avator.webp';
        img.alt = 'Yui';
        avatar.appendChild(img);
    } else {
        avatar.textContent = '你';
    }
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    // 滚动到底部
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 显示加载动画
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai';
    typingDiv.id = 'typingIndicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    const img = document.createElement('img');
    img.src = '/static/img/yui_avator.webp';
    img.alt = 'Yui';
    avatar.appendChild(img);
    
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    
    typingDiv.appendChild(avatar);
    typingDiv.appendChild(indicator);
    chatMessages.appendChild(typingDiv);
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 移除加载动画
function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// 发送消息到后端
async function sendMessage(message) {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || '请求失败');
        }
        
        return data.response;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// 清除对话历史
async function clearChat() {
    if (confirm('确定要清除所有对话记录吗？')) {
        try {
            const response = await fetch('/api/clear', {
                method: 'POST'
            });
            
            if (response.ok) {
                // 清空聊天区域，保留欢迎消息
                const messages = chatMessages.querySelectorAll('.message');
                messages.forEach(msg => msg.remove());
                
                // 重新添加欢迎消息
                const welcomeDiv = document.createElement('div');
                welcomeDiv.className = 'welcome-message';
                welcomeDiv.innerHTML = `
                    <div class="welcome-avatar">
                        <img src="/static/img/yui_avator.webp" alt="Yui">
                    </div>
                    <div class="welcome-text">
                        <p>对话已清除。有什么新的问题我可以帮你分析吗？</p>
                    </div>
                `;
                chatMessages.insertBefore(welcomeDiv, chatMessages.firstChild);
            }
        } catch (error) {
            console.error('清除对话失败:', error);
            alert('清除对话失败，请重试');
        }
    }
}

// 处理表单提交
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    
    if (!message || isWaiting) return;
    
    // 禁用输入和按钮
    isWaiting = true;
    messageInput.disabled = true;
    sendBtn.disabled = true;
    
    // 添加用户消息
    addMessage(message, 'user');
    messageInput.value = '';
    
    // 显示加载动画
    showTypingIndicator();
    
    try {
        // 发送消息并等待响应
        const response = await sendMessage(message);
        
        // 移除加载动画
        removeTypingIndicator();
        
        // 添加 AI 回复
        addMessage(response, 'ai');
    } catch (error) {
        removeTypingIndicator();
        addMessage('抱歉，我遇到了一些问题。请稍后再试。', 'ai');
        console.error('发送消息失败:', error);
    } finally {
        // 恢复输入和按钮
        isWaiting = false;
        messageInput.disabled = false;
        sendBtn.disabled = false;
        messageInput.focus();
    }
});

// 清除按钮点击事件
clearBtn.addEventListener('click', clearChat);

// 回车键发送（Shift+Enter 换行）
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// 页面加载完成后聚焦输入框
window.addEventListener('load', () => {
    messageInput.focus();
});
