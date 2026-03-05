import torch
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import time

start = time.time()

embeddings = HuggingFaceEmbeddings(
    model_name='tbs17/MathBERT'#"Qwen/Qwen2.5-3B-Instruct",
    # model_kwargs={"trust_remote_code": True, "device": device}
    )
vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
# 仅在你完全信任 faiss_index 文件的来源时，才将 allow_dangerous_deserialization 设置为 True

print("time1:",time.time() - start,"\n")

# 加载模型和分词器
model_id = "Qwen/Qwen2-0.5B"#"Qwen/Qwen2.5-3B-Instruct"  # 使用支持生成的因果语言模型
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",  # 自动分配设备
    torch_dtype=torch.bfloat16  # 节省显存
)

# 创建推理管道
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=512,
    temperature=0.5
)

# 初始化大语言模型
llm = HuggingFacePipeline(pipeline=pipe)

print("time2:",time.time() - start,"\n")

# 定义Prompt模板

# 如果上下文不包含相关信息，请明确告知"根据已知信息无法回答该问题"。
prompt_template = """
你是一个专业的问答助手，请参考上下文回答问题。

上下文：
{context}

问题：{input}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

print("time3:",time.time() - start,"\n")

# 创建文档链
document_chain = create_stuff_documents_chain(llm, prompt)

# 创建检索链
retriever = vector_db.as_retriever(search_kwargs={"k": 10})  # 检索结果
rag_chain = create_retrieval_chain(retriever, document_chain)

# 输入问题
query = "一个50度的扇形，半径为5cm，其面积为多少？"

print("time4:",time.time() - start,"\n")

# 运行RAG流程
response = rag_chain.invoke({"input": query})

print("response 字典的键:", response.keys())

# 打印结果
print("=== 检索到的上下文 ===")
for doc in response["context"]:
    source = doc.metadata.get('source', '未知')
    page = doc.metadata.get('page', '未知')
    if isinstance(page, int):
        page_str = str(page + 1)
    else:
        page_str = page
    print(f"来源：{source} (第{page_str}页)")
    print(doc.page_content[:200] + "...\n")

print("time5:",time.time() - start,"\n")

print("\n=== 生成答案 ===")
print(response["answer"])

print("time6:",time.time() - start,"\n")