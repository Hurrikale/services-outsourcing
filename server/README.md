# AI聊天应用

基于Flask和Qwen2.5-Math模型的智能问答系统，支持多轮对话和上下文理解。

## 功能特点

- 🤖 集成Qwen2.5-Math模型，支持智能问答
- 💬 支持多轮对话，自动保存对话历史
- 🎨 现代化的用户界面，支持深色/浅色主题切换
- 👥 多用户支持，独立的用户聊天记录
- 📱 响应式设计，支持移动端访问

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 初始化数据库

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

### 3. 导入初始数据

从 <mcfile name="import_data.py" path="f:\list\250325\import_data.py"></mcfile> 可以看出，该脚本用于导入数据目录下的数据到数据库中：

```bash
python import_data.py
```

这个脚本会连接到MySQL数据库，创建必要的表，并从`./data`目录导入数据文件。


4. 配置环境变量：
创建`config.py`文件并填写以下配置：


6. 初始化数据库：
```bash
flask db init
flask db migrate
flask db upgrade
```

## 运行应用

1. 启动服务器：
```bash
python app.py
```

2. 访问应用：
打开浏览器访问 http://127.0.0.1:5000

## 使用说明

1. 注册/登录：
   - 首次使用需要注册账号
   - 使用邮箱和密码登录

2. 开始对话：
   - 点击"新建聊天"创建新的对话
   - 在输入框输入问题并发送
   - AI会自动生成回答

3. 管理对话：
   - 左侧边栏显示所有对话历史
   - 点击对话可以切换
   - 可以重命名或删除对话

4. 用户设置：
   - 右上角设置按钮可以切换主题
   - 支持注销账号

## 技术栈

- 后端：Flask + SQLAlchemy
- 前端：HTML + CSS + JavaScript
- 数据库：MySQL
- AI模型：Qwen2.5-Math (基于transformers)

## 目录结构

```
.
├── app.py              # 主应用入口
├── config.py           # 配置文件
├── models.py           # 数据库模型
├── exts.py            # 扩展初始化
├── decorators.py      # 装饰器
├── database.sql       # 数据库结构
├── requirements.txt   # 依赖列表
├── static/           # 静态文件
│   ├── styles.css    # 样式表
│   └── script.js     # 前端脚本
├── templates/        # 模板文件
│   └── index.html    # 主页面
└── rag_model/        # RAG模型相关
    ├── rag_engine.py # RAG引擎
    └── model_utils.py # 模型工具
```

## 注意事项

1. 首次运行时会自动下载AI模型，需要较好的网络环境
2. 建议使用GPU进行模型推理，CPU推理可能较慢
3. 确保MySQL服务已启动并正确配置
4. 注意保护.env文件中的敏感信息

## 常见问题

1. 模型下载失败：
   - 检查网络连接
   - 确保有足够的磁盘空间

2. 数据库连接错误：
   - 检查MySQL服务是否启动
   - 验证数据库配置信息

3. 依赖安装问题：
   - 使用`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`尝试国内镜像
   - 确保Python版本兼容
