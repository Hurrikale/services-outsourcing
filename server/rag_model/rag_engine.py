from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain_community.embeddings import HuggingFaceEmbeddings  # 新增导入
from typing import List, Dict, Any
from rag_model.db_utils import DatabaseManager
from langchain_community.vectorstores import FAISS
import torch
from utils.logger import logger
import functools
import time
import os

def load_vector_db(embeddings):
    """加载向量数据库"""
    try:
        vector_db = FAISS.load_local("./rag_model/faiss_index", embeddings, allow_dangerous_deserialization=True)
        # print("Success")
        return vector_db
    except Exception as e:
        logger.info(f"加载向量数据库时出现错误: {e}")
        return None

def log_rag_process(func):
    """记录 RAG 处理过程的装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"[RAG] 开始执行 {func.__name__}")
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(f"[RAG] 成功完成 {func.__name__}, 耗时: {end_time - start_time:.2f}秒")
            return result
        except Exception as e:
            logger.error(f"[RAG] {func.__name__} 失败: {str(e)}", exc_info=True)
            raise
    return wrapper

# 在类定义前添加常量
MAX_CONTEXT_LENGTH = 3000  # 最大上下文长度
MAX_HISTORY_ITEMS = 3      # 最多使用3条历史记录

class RAGEngine:
    def __init__(self):
        logger.info("[RAG] 初始化 RAG 引擎")
        self.db = DatabaseManager()
        # ...其他初始化代码...
        self.conversation_history = []  # 存储格式：(question, answer)
        self.model_path = "./rag_model/models/Qwen/Qwen2.5-Math-1.5B-Instruct"
        self.model = None
        self.tokenizer = None
        # 检查是否有可用的 GPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # 正确初始化embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_path,
            model_kwargs={'device': self.device}
        )
        # 在RAGEngine初始化中增加安全验证
        self.db.init_vector_db(load_vector_db(self.embeddings))  # 替换原来的直接赋值
        logger.info(f"[RAG] 使用设备: {self.device}")
        # 系统提示
        self.SYSTEM_PROMPT = """你是一位数学专家，请严格遵循：
        1. 使用中文逐步推理，解释关键概念
        2. 计算问题必须展示完整推导过程
        3. 最终答案用 \\boxed{} 标注
        4. 禁止使用编程工具，仅用数学推导
        5. 几何问题可描述辅助线，无需绘图代码
        """

    @log_rag_process
    def load_model(self):
        """改进的模型加载方法"""
        logger.info("[RAG] 开始加载模型...")
        try:
            # 明确指定设备，避免碎片化加载
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
            
            # 加载分词器
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            # 加载模型 - 明确指定设备
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                device_map=device,  # 明确指定设备
                trust_remote_code=True,
                torch_dtype=torch.float16 if "cuda" in device else torch.float32
            ).eval()  # 设置为评估模式
            
            logger.info(f"[RAG] 模型成功加载到设备: {device}")
            return True
        except Exception as e:
            logger.error(f"[RAG] 模型加载失败: {str(e)}", exc_info=True)
            return False

    @log_rag_process
    def generate_answer(self, question: str, chat_id: int) -> str:
        """改进的答案生成方法"""
        try:
            if not self.is_ready():
                raise RuntimeError("模型未加载")
            
            # 1. 获取历史记录（限制数量）
            self.conversation_history = self.db.get_history(chat_id)[-MAX_HISTORY_ITEMS:]
            
            # 2. 检索相关上下文（添加相关性过滤）
            contexts = self.db.search_similar_contexts(question)
            # 过滤低质量上下文
            filtered_contexts = contexts
            
            # 3. 构建高效提示
            prompt = self._build_prompt(question, filtered_contexts)

            print(prompt)
            
            logger.info(f"[RAG] 提示长度: {len(prompt)} 字符")
            
            # 4. 生成答案（优化参数）
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            
            # 关键：使用更确定的生成参数
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,  # 减少生成长度
                do_sample=True,
                temperature=0.3,     # 降低随机性
                top_p=0.85,          # 限制采样范围
                top_k=40,            # 添加top_k过滤
                repetition_penalty=1.25,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,  # 使用eos作为pad
                eos_token_id=self.tokenizer.eos_token_id
            )
            
            # 5. 提取并清理答案
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            answer = full_response[len(prompt):].strip()
            
            # 关键：后处理确保格式正确
            return self._postprocess_answer(answer)
            
        except Exception as e:
            logger.error(f"[RAG] 生成答案失败: {str(e)}", exc_info=True)
            return f"抱歉，处理问题时出错: {str(e)}"

    def _build_prompt(self, question: str, contexts: List[Dict]) -> str:
        """构建高效提示"""
        # 1. 系统指令
        prompt = f"<|system|>\n{self.SYSTEM_PROMPT}</s>\n"
        
        # 2. 添加上下文（如果有）
        if contexts:
            prompt += "<|context|>\n"
            for i, ctx in enumerate(contexts, 1):
                prompt += f"[参考{i}]: {ctx['content'][:200]}"  # 截断长文本
                if i < len(contexts):
                    prompt += "\n"
            prompt += "</s>\n"
        
        # 3. 添加历史对话（角色明确）
        if self.conversation_history:
            prompt += "<|history|>\n"
            for q, a in self.conversation_history:
                prompt += f"用户: {q}\n"
                prompt += f"助手: {a}\n"
            prompt += "</s>\n"
        
        # 4. 当前问题
        prompt += f"<|user|>\n{question}</s>\n"
        prompt += "<|assistant|>\n"
        
        return prompt

    def _postprocess_answer(self, answer: str) -> str:
        """答案后处理"""
        # 1. 移除可能的重复前缀
        prefixes = ["助手:", "assistant:"]
        for prefix in prefixes:
            if answer.startswith(prefix):
                answer = answer[len(prefix):].strip()
        
        # 2. 确保包含boxed答案
        if "\\boxed" not in answer:
            # 尝试在结尾添加
            if answer.strip().endswith("."):
                answer = answer[:-1] + " \\boxed{}"
            else:
                answer += " \\boxed{}"
        
        # 3. 截断过长答案
        if len(answer) > 1500:
            answer = answer[:1400] + "\n...（回答过长被截断）"
        
        return answer

    def is_ready(self) -> bool:
        """检查模型是否准备就绪"""
        try:
            if self.model is None or self.tokenizer is None:
                logger.warning("[RAG] 模型或分词器未加载")
                return False
            return True
        except Exception as e:
            logger.error(f"[RAG] 检查模型状态时出错: {str(e)}", exc_info=True)
            return False


if __name__ == "__main__":
    # 测试RAG引擎
    engine = RAGEngine()
    try:
        engine.load_model()
        result = engine.generate_answer("什么是勾股定理？")
        print(f"测试回答: {result}")
    except Exception as e:
        print(f"测试失败: {str(e)}")