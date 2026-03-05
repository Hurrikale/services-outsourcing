# 数学RAG问答系统

基于Qwen2.5-Math模型和MySQL知识库的数学问答系统。

## 系统组件

1. 知识库
   - MySQL数据库 (function数据库)
   - context表存储数学题目和解析
   - 支持文本相似度检索

2. 模型层
   - Qwen2.5-Math-1.5B-Instruct
   - RAG检索增强生成
   - 支持数学公式理解

3. Web界面
   - Streamlit实现
   - 实时问答功能
   - 历史记录查看

## 项目结构

- `main.py`: Streamlit应用入口
- `rag_engine.py`: RAG核心逻辑实现
- `db_utils.py`: 数据库操作工具
- `model_utils.py`: 模型下载和管理
- `import_data.py`: 数据导入工具
- `requirements.txt`: 项目依赖

## 使用说明

1. 启动应用：
```bash
streamlit run main.py
```

2. 访问界面：
- 打开浏览器访问 http://localhost:8501
- 在输入框中输入数学问题
- 点击提交获取答案
- 查看历史记录了解之前的问答

## 技术栈

- 模型: Qwen2.5-Math-1.5B-Instruct
- 数据库: MySQL
- 框架: Streamlit
- 编程语言: Python
- 核心库: modelscope, transformers, torch
