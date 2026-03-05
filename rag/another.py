# 安装必要库（运行前取消注释）
# !pip install transformers sentence-transformers faiss-cpu torch

from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch

class QwenRAGSystem:
    def __init__(self, knowledge_base=None, max_history=3):
        # 初始化Qwen2模型
        self.model_name = "Qwen/Qwen2-7B-Instruct"  # 根据实际模型调整
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name, 
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        
        # 知识库设置
        self.knowledge_base = knowledge_base or [
            "爱因斯坦于1905年提出狭义相对论，1915年完成广义相对论。",
            "Python 3.12于2023年10月发布，改进了错误提示和类型系统。",
            "国际空间站运行在距离地面约400公里的低地球轨道上。"
        ]
        
        # 检索系统初始化
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self._build_faiss_index()
        
        # 对话历史管理
        self.max_history = max_history
        self.history = []

    def _build_faiss_index(self):
        # 构建知识库向量索引
        embeddings = self.embedder.encode(self.knowledge_base, normalize_embeddings=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings.astype(np.float32))

    def _retrieve_documents(self, query, k=3):
        # 检索相关文档
        query_embed = self.embedder.encode([query], normalize_embeddings=True)
        distances, indices = self.index.search(query_embed.astype(np.float32), k)
        return [self.knowledge_base[i] for i in indices[0]]

    def _format_prompt(self, question, context):
        # 使用Qwen2的指令格式模板
        history_str = "\n".join([f"问：{q}\n答：{a}" for q, a in self.history])
        context_str = "\n".join(context)
        
        return f"""<|im_start|>system
你是一个智能助手，请基于以下上下文信息回答问题：
{context_str}

历史对话记录：
{history_str}<|im_end|>
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant
"""

    def generate_response(self, question, max_new_tokens=512):
        # 1. 检索相关知识
        context = self._retrieve_documents(question)
        
        # 2. 构建符合Qwen2格式的prompt
        prompt = self._format_prompt(question, context)
        
        # 3. 生成回答
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            inputs.input_ids,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        # 4. 解码并清理输出
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer = full_response.split("<|im_start|>assistant\n")[-1].strip()
        
        # 5. 更新对话历史
        self.history.append((question, answer))
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        return answer

# 使用示例
rag = QwenRAGSystem()

questions = [
    "爱因斯坦最重要的贡献是什么？",
    "这些理论分别是哪年提出的？",  # 测试上下文保持
    "Python最新版本有什么改进？"
]

for q in questions:
    print(f"用户：{q}")
    print(f"助手：{rag.generate_response(q)}\n")