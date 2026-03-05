// js/main.js

// 定义 submitQuestion 函数，用于提交用户输入的问题并处理响应
function submitQuestion() {
  // 获取用户在输入框中输入的内容
  let userInput = document.getElementById('user-input').value;

  // 使用 fetch API 向指定的 API 端点发送 POST 请求
  fetch('https://api.example.com/v1/chat/completions', {
      // 请求方法为 POST
      method: 'POST',
      // 设置请求头，包含授权信息和内容类型
      headers: {
          'Authorization': 'Bearer YOUR_API_KEY',
          'Content-Type': 'application/json'
      },
      // 将请求数据转换为 JSON 字符串并作为请求体发送
      body: JSON.stringify({
          // 指定使用的模型
          model: 'Qwen2-Math-7B-Instruct',
          // 包含用户消息的数组，消息包含角色和内容
          messages: [{ role: 'user', content: userInput }],
          // 最大生成的令牌数
          max_tokens: 500
      })
  })
  // 处理响应，将响应数据解析为 JSON 格式
  .then(response => response.json())
  // 处理解析后的 JSON 数据
  .then(data => {
      // 从响应数据中提取答案内容
      let answer = data.choices[0].message.content;
      // 将答案显示在页面上的指定元素中
      document.getElementById('answer').innerText = answer;
      // 显示答案容器
      document.getElementById('answer-container').style.display = 'block';
      // 调用 getRelatedQuestions 函数，获取相关问题
      getRelatedQuestions(userInput);
      // 调用 getReferenceFiles 函数，获取参考文件
      getReferenceFiles(userInput);
  })
  // 捕获并处理请求过程中可能出现的错误
  .catch(error => console.error('Error:', error));
}

// 定义 getRelatedQuestions 函数，用于获取与用户问题相关的问题
function getRelatedQuestions(question) {
  // 使用 fetch API 向指定的 API 端点发送 POST 请求
  fetch('https://api.example.com/v1/related_questions', {
      // 请求方法为 POST
      method: 'POST',
      // 设置请求头，包含授权信息和内容类型
      headers: {
          'Authorization': 'Bearer YOUR_API_KEY',
          'Content-Type': 'application/json'
      },
      // 将问题数据转换为 JSON 字符串并作为请求体发送
      body: JSON.stringify({ question })
  })
  // 处理响应，将响应数据解析为 JSON 格式
  .then(response => response.json())
  // 处理解析后的 JSON 数据
  .then(data => {
      // 获取页面上用于显示相关问题的列表元素
      let relatedQuestionsList = document.getElementById('related-questions-list');
      // 清空列表内容
      relatedQuestionsList.innerHTML = '';
      // 遍历响应数据中的相关问题数组
      data.related_questions.forEach(q => {
          // 创建一个列表项元素
          let li = document.createElement('li');
          // 将问题内容设置为列表项的文本
          li.innerText = q;
          // 将列表项添加到相关问题列表中
          relatedQuestionsList.appendChild(li);
      });
  });
}

// 定义 getReferenceFiles 函数，用于获取与用户问题相关的参考文件
function getReferenceFiles(question) {
  // 使用 fetch API 向指定的 API 端点发送 GET 请求
  fetch('https://api.example.com/v1/reference_files?question_id=123', {
      // 请求方法为 GET
      method: 'GET',
      // 设置请求头，包含授权信息和内容类型
      headers: {
          'Authorization': 'Bearer YOUR_API_KEY',
          'Content-Type': 'application/json'
      }
  })
  // 处理响应，将响应数据解析为 JSON 格式
  .then(response => response.json())
  // 处理解析后的 JSON 数据
  .then(data => {
      // 获取页面上用于显示参考文件的列表元素
      let referenceFilesList = document.getElementById('reference-files-list');
      // 清空列表内容
      referenceFilesList.innerHTML = '';
      // 遍历响应数据中的参考文件数组
      data.reference_files.forEach(file => {
          // 创建一个列表项元素
          let li = document.createElement('li');
          // 将文件内容设置为列表项的文本
          li.innerText = file;
          // 将列表项添加到参考文件列表中
          referenceFilesList.appendChild(li);
      });
  });
}