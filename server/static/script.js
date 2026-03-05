let chats = JSON.parse(localStorage.getItem('chats')) || [];
let currentChatId = null;

// 配置 MathJax
// window.MathJax = {
//   tex: {
//     inlineMath: [['$', '$'], ['\\(', '\\)']],  // 行内公式符号
//     displayMath: [['$$', '$$'], ['\\[', '\\]']], // 块级公式符号
//     packages: {'[+]': ['ams']},                // 启用 amsmath 扩展（支持 \boxed{}）
//     processEscapes: true,                      // 允许反斜杠转义
//     tags: 'ams'                                // 自动编号公式
//   },
//   startup: {
//     typeset: false                             // 禁用自动渲染
//   },
//   options: {
//     renderActions: {
//       addMenu: [0, '', '']                     // 隐藏右键菜单
//     }
//   }
// };

// 创建新聊天
async function startNewChat() {
  const newChat = {
    id: null,
    time: Date.now(),
    name: '新聊天',
    messages: [{ sender: 'AI', message: '你好！有什么我可以帮助的吗？' }],
    date: new Date()
  };
  const response = await fetch('/chat/new', {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
    },
    body: JSON.stringify( newChat )
  });
  const data = await response.json();
  if (data.code !== 200) {
      // 存入数据库失败
      alert(data.message);
      return;
  }
  newChat.id = data.id;
  newChat.name = newChat.name + data.number
  // 将新聊天插入到数组的最前面
  chats.unshift(newChat);
  localStorage.setItem('chats', JSON.stringify(chats));

  const chatItem = createChatItem(newChat);
  const chatList = document.getElementById('chatList');
  chatList.insertBefore(chatItem, chatList.firstChild); // 插入到顶部

  showChatContent(newChat);
}

// 优化版的打字机效果函数（减少重渲染）
function typeWriterEffect(text, element) {
  const chatWindow = document.getElementById('chatWindow');
  let i = 0;
  const speed = 20; // 打字速度（毫秒）
  const renderInterval = 5; // 每5个字符渲染一次
  let lastRenderIndex = 0;
  
  // 清空元素内容
  element.innerHTML = '';
  
  // 开始打字效果
  function type() {
    if (i < text.length) {
      i++;
      
      // 只在需要时渲染（减少渲染频率）
      if (i - lastRenderIndex >= renderInterval || i === text.length) {
        // 获取当前文本
        const currentText = text.substring(0, i);
        
        // 1. 使用占位符保护LaTeX公式
        let processedText = currentText
          .replace(/\\\[/g, '！^！START_FORMULA！^！')
          .replace(/\\\]/g, '！^！END_FORMULA！^！')
          .replace(/\\\(/g, '！%！START_FORMULA！%！')
          .replace(/\\\)/g, '！%！END_FORMULA！%！');
        
        // 2. 渲染Markdown
        let markdownHTML = DOMPurify.sanitize(marked.parse(processedText));
        
        // 3. 还原LaTeX公式
        markdownHTML = markdownHTML
          .replace(/！\^！START_FORMULA！\^！/g, '\\[')
          .replace(/！\^！END_FORMULA！\^！/g, '\\]')
          .replace(/！%！START_FORMULA！%！/g, '\\(')
          .replace(/！%！END_FORMULA！%！/g, '\\)');
        
        // 4. 更新元素内容
        element.innerHTML = markdownHTML;
        
        // 5. 渲染数学公式
        MathJax.typesetPromise([element]).catch((err) => console.error(err));
        
        lastRenderIndex = i;
      }
      
      // 滚动到底部
      chatWindow.scrollTop = chatWindow.scrollHeight;
      setTimeout(type, speed);
    } else {
      // 确保最终渲染正确
      let processedText = text
        .replace(/\\\[/g, '！^！START_FORMULA！^！')
        .replace(/\\\]/g, '！^！END_FORMULA！^！')
        .replace(/\\\(/g, '！%！START_FORMULA！%！')
        .replace(/\\\)/g, '！%！END_FORMULA！%！');
      
      let finalHTML = DOMPurify.sanitize(marked.parse(processedText));
      
      finalHTML = finalHTML
        .replace(/！\^！START_FORMULA！\^！/g, '\\[')
        .replace(/！\^！END_FORMULA！\^！/g, '\\]')
        .replace(/！%！START_FORMULA！%！/g, '\\(')
        .replace(/！%！END_FORMULA！%！/g, '\\)');
      
      element.innerHTML = finalHTML;
      MathJax.typesetPromise([element]).catch((err) => console.error(err));
    }
  }
  
  type();
}

// 发送消息
async function sendMessage() {
  const input = document.getElementById('chatInput');
  const message = input.value.trim();
  if (message) {
    const currentChat = chats.find(chat => chat.id === currentChatId);
    // 先更新用户输出
    currentChat.messages.push({ sender: 'user', message: message });
    showChatContent(currentChat);
    $('#thinkingIndicator').show();
    $('#sendBtn').hide();
    input.value = '';

    // 创建AI消息占位元素
    const chatWindow = document.getElementById('chatWindow');
    const aiMessageElement = document.createElement('div');
    aiMessageElement.classList.add('message', 'ai-message');
    aiMessageElement.id = 'ai-response';
    chatWindow.appendChild(aiMessageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight; // 滚动到底部

    // 将当前聊天移动到数组的最前面
    chats = chats.filter(chat => chat.id !== currentChatId);
    chats.unshift(currentChat);
    localStorage.setItem('chats', JSON.stringify(chats));

    try{
      const response = await fetch('/sendmessage', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({
          question: message,
          chat_id: currentChatId
        }),
        timeout: 1200000, // 设置20分钟超时
        error: function(xhr, status, error) {
            if (status === 'timeout') {
                throw new Error('请求超时，请稍后重试');
            } else if (xhr.status === 0) {
                throw new Error('无法连接到服务器，请检查网络连接');
            } else {
                throw new Error(`请求失败: ${error}`);
            }
        }
      });
      const data = await response.json();
      // 隐藏思考中的提示
      $('#thinkingIndicator').hide();
      $('#sendBtn').show(); 

      if (data.code !== 200) {
        // 存入数据库失败
        alert(data.message);
        return;
      }

      // 使用打字机效果显示AI响应
      typeWriterEffect(data.result, aiMessageElement);
      
      // 更新聊天记录
      currentChat.messages.push({ sender: 'AI', message: data.result });
    }
    catch (error) {
      // 隐藏思考中的提示
      $('#thinkingIndicator').hide();
      $('#sendBtn').show();

      // 显示错误信息
      aiMessageElement.textContent = `抱歉，发生错误：${error.message || '未知错误'}`;
      
      // 记录错误到控制台
      console.error('发送消息失败:', error);
    }
    
    // 更新聊天列表
    updateChatList();
  }
}

// 创建聊天项 DOM 元素
function createChatItem(chat) {
  // console.log(chat)
  const chatItem = document.createElement('li');
  chatItem.textContent = chat.name;
  chatItem.classList.add('chat-item');  // 统一添加类名
  chatItem.setAttribute('data-chat-id', chat.id);  // 用于查找
  chatItem.onclick = () => showChatContent(chat);

  // 添加选项按钮
  const optionsBtn = document.createElement('button');
  optionsBtn.textContent = '⋮';
  optionsBtn.classList.add('options-btn');
  optionsBtn.onclick = (event) => {
    event.stopPropagation(); // 防止触发li的onclick事件
    showOptions(chat, event); // 传递event获取鼠标位置
  };
  chatItem.appendChild(optionsBtn);

  return chatItem;
}


// 显示聊天内容
function showChatContent(chat) {
  const chatWindow = document.getElementById('chatWindow');
  chatWindow.innerHTML = '';
  currentChatId = chat.id;

  // 清除旧的高亮
  document.querySelectorAll('.chat-item').forEach(item => {
    item.classList.remove('active-chat');
  });

  // 高亮当前选中的聊天项
  const activeChatItem = document.querySelector(`[data-chat-id="${chat.id}"]`);
  if (activeChatItem) {
    activeChatItem.classList.add('active-chat');
  }

  // // 处理答案中的数学公式和步骤
  // let formattedAnswer = data.result
  // .replace(/\\boxed{([^}]+)}/g, '<div class="math-formula">$1</div>')
  // .replace(/(\d+\.\s+[^\n]+)/g, '<div class="step">$1</div>')
  // .replace(/(最终答案[：:]\s*[^\n]+)/g, '<div class="final-answer">$1</div>');

  // // 重新渲染数学公式
  // MathJax.typeset();
  // 显示聊天记录
  chat.messages.forEach(message => {
    // 临时替换 \[ 和 \]
    let processedMessage = message.message.replace(/\\\[/g, '！^！START_FORMULA！^！').replace(/\\\]/g, '！^！END_FORMULA！^！').replace(/\\\(/g, '！%！START_FORMULA！%！').replace(/\\\)/g, '！%！END_FORMULA！%！');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${message.sender.toLowerCase()}-message`);
    messageElement.innerHTML = DOMPurify.sanitize(marked.parse(processedMessage));
    // 把临时占位符替换回来
    messageElement.innerHTML = messageElement.innerHTML.replace(/！\^！START_FORMULA！\^！/g, '\\[').replace(/！\^！END_FORMULA！\^！/g, '\\]').replace(/！%！START_FORMULA！%！/g, '\\(').replace(/！%！END_FORMULA！%！/g, '\\)');
    // 使用 MathJax 3 的 API 渲染公式
    chatWindow.appendChild(messageElement);
    MathJax.typesetPromise([messageElement]).catch((err) => console.error(err));
  });

  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// 更新聊天记录列表
async function updateChatList(tag = 0) {
  if (tag) {
    localStorage.removeItem('chats');
    chats = []
    const response = await fetch('/firstquery', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
      }
    });
    const data = await response.json();
    if (data.code !== 200) {
      // 存入数据库失败
      alert(data.message);
      return;
    }
    // console.log(data);
    for (const item of data['result']) {

      // 将新聊天插入到数组的最前面
      item.date = new Date()
      chats.push(item);
      localStorage.setItem('chats', JSON.stringify(chats));

      const chatItem = createChatItem(item);
      const chatList = document.getElementById('chatList');
      chatList.insertBefore(chatItem, chatList.firstChild); // 插入到顶部

    }
    init();
  }
  // localStorage.removeItem('chats');
  const chatList = document.getElementById('chatList'); // 假设 HTML 中有一个 <ul id="chatList"> 用于显示所有聊天
  chatList.innerHTML = ''; // 清空现有列表

  // 按时间排序（最新的在前面，chats 数组已按此顺序维护）
  chats.forEach(chat => {
    const chatItem = createChatItem(chat);
    chatItem.setAttribute('data-chat-id', chat.id);
    chatList.appendChild(chatItem);
  });

  // 恢复高亮
  if (currentChatId) {
    const activeChatItem = document.querySelector(`[data-chat-id="${currentChatId}"]`);
    if (activeChatItem) {
      activeChatItem.classList.add('active-chat');
    }
  }
}

// 在页面加载时默认进入最近的对话
function init() {
  // const chatWindow = document.getElementById('chatWindow');
  // chatWindow.innerHTML = '';
  // 获取最近的聊天记录
  const recentChat = chats[0];  // 默认最新的聊天在数组的开头
  if (recentChat) {
    // 显示最近的聊天内容
    showChatContent(recentChat);

    // 确保 DOM 渲染完成后再高亮
    setTimeout(() => {
      // 高亮当前选中的聊天项
      const activeChatItem = document.querySelector(`[data-chat-id="${recentChat.id}"]`);
      if (activeChatItem) {
        activeChatItem.classList.add('active-chat');
      }
    }, 0);  // 延迟到事件队列的下一轮执行
  }
}


// 显示重命名或删除选项
async function showOptions(chat, event) {
  // 创建一个选项菜单
  const optionsMenu = document.createElement('div');
  optionsMenu.classList.add('options-menu');

  // 添加输入框用于直接编辑名称
  const renameInput = document.createElement('input');
  renameInput.value = chat.name;
  optionsMenu.appendChild(renameInput);

  const closeMenu = () => {
    if (document.body.contains(optionsMenu)) {
      document.body.removeChild(optionsMenu);
    }
    document.removeEventListener('click', onDocumentClick);
  };

  const onDocumentClick = (e) => {
    if (!optionsMenu.contains(e.target) && e.target !== event.target) {
      closeMenu();
    }
  };

  const saveRenameOption = document.createElement('button');
  saveRenameOption.textContent = '保存';
  saveRenameOption.onclick = async (e) => {
    e.stopPropagation();
    const newName = renameInput.value.trim();
    if (newName) {
      const response = await fetch('/rename', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({ currentChatId: chat.id, newName })
      });
      const data = await response.json();
      if (data.code !== 200) {
        // 存入数据库失败
        alert(data.message);
        return;
      }
      chat.name = newName;
      localStorage.setItem('chats', JSON.stringify(chats));
      updateChatList();
      // 如果这是当前聊天，保持选中状态
      if (chat.id === currentChatId) {
        showChatContent(chat); // 刷新内容并高亮
      }
    }
    closeMenu(); // 移除菜单
  };

  const deleteOption = document.createElement('button');
  deleteOption.textContent = '删除';
  deleteOption.onclick = async (e) => {
    if (confirm('确定要删除该聊天记录吗？')) {
      e.stopPropagation();
      const response = await fetch('/delete', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({ currentChatId: chat.id })
      });
      const data = await response.json();
      if (data.code !== 200) {
        // 存入数据库失败
        alert(data.message);
        return;
      }
      const wasCurrentChat = (chat.id === currentChatId); // 记录是否删除的是当前聊天
      chats = chats.filter(c => c.id !== chat.id);
      localStorage.setItem('chats', JSON.stringify(chats));
      updateChatList();
      if (wasCurrentChat && chats.length > 0) {
        // 如果删除的是当前聊天，自动选中最新聊天
        currentChatId = chats[0].id;
        showChatContent(chats[0]);
      } else if (chats.length === 0) {
        currentChatId = null;
        document.getElementById('chatWindow').innerHTML = ''; // 清空聊天窗口
      }
      closeMenu();
    }
  };

  optionsMenu.appendChild(saveRenameOption);
  optionsMenu.appendChild(deleteOption);

  // 显示菜单，设置位置为点击事件的鼠标位置
  optionsMenu.style.position = 'absolute';
  optionsMenu.style.left = `${event.clientX}px`;
  optionsMenu.style.top = `${event.clientY}px`;

  // 将菜单添加到 body
  document.body.appendChild(optionsMenu);
  requestAnimationFrame(() => {
    document.addEventListener('click', onDocumentClick);
  });
}

// 模型选择
function changeModel() {
  const selectedModel = document.getElementById('modelSelect').value;
  console.log(`Selected model: ${selectedModel}`);
}

// 获取按钮和弹窗元素
const userSettingsButton = document.getElementById('userSettingsButton');
const settingsModal = document.getElementById('settingsModal');
const closeButton = document.getElementById('closeButton');
const toggleThemeButton = document.getElementById('toggleTheme');
const logoutButton = document.getElementById('logoutButton');
const body = document.body;

// 检查并应用保存的主题模式
function applySavedTheme() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    body.classList.add('dark-mode');
    toggleThemeButton.textContent = '切换到白天模式';
  } else {
    body.classList.remove('dark-mode');
    toggleThemeButton.textContent = '切换到黑夜模式';
  }
}

// 打开弹窗
userSettingsButton.addEventListener('click', () => {
  settingsModal.style.display = 'block';
});

// 关闭弹窗
closeButton.addEventListener('click', () => {
  settingsModal.style.display = 'none';
});

// 切换主题模式
toggleThemeButton.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
  if (body.classList.contains('dark-mode')) {
    toggleThemeButton.textContent = '切换到白天模式';
    localStorage.setItem('theme', 'dark'); // 保存暗夜模式
  } else {
    toggleThemeButton.textContent = '切换到黑夜模式';
    localStorage.setItem('theme', 'light'); // 保存白天模式
  }
});

// 在页面加载时调用
applySavedTheme();

// 注销账号
logoutButton.addEventListener('click', () => {
  window.location.href = "/auth/logout";
  settingsModal.style.display = 'none'; // 关闭弹窗
});

// 点击弹窗外部区域关闭弹窗
window.onclick = function(event) {
  if (event.target === settingsModal) {
    settingsModal.style.display = 'none';
  }
};

// 回车发送消息
function handleKeyPress(event) {
  if (event.key === 'Enter') {
    sendMessage();
  }
}

// 初始化
updateChatList(1);