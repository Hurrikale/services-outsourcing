import torch
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import time
import mysql.connector
from langchain_core.prompts import MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage

# todo : 合并时删除这一部分
DB_CONFIG = {
    'user': 'root',
    'password': 'F0r_5ErV1<E_0u7s0ur<1n6',
    'host': '127.0.0.1',
    'database': 'mydatabase',
    'raise_on_warnings': True
}

def delete_all_records():
    """删除 TempModel 表中的所有记录"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    delete_query = "DELETE FROM temporary"
    cursor.execute(delete_query)
    conn.commit()
    cursor.close()
    conn.close()

def get_all_records():
    """获取 TempModel 表中的所有记录"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    select_query = "SELECT question, answer FROM temporary"
    cursor.execute(select_query)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

def add_record(question, answer):
    """向 TempModel 表中添加一条记录"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    insert_query = "INSERT INTO temporary (question, answer) VALUES (%s, %s)"
    cursor.execute(insert_query, (question, answer))
    conn.commit()
    cursor.close()
    conn.close()


def load_model_and_tokenizer(model_id):
    """加载模型和分词器"""
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",  # 自动分配设备
        torch_dtype=torch.float16  # 节省显存
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        trust_remote_code=True,
        truncation=True,
    )
    return model, tokenizer


def create_inference_pipeline(model, tokenizer):
    """创建推理管道"""
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,  # 确保最大长度不超过模型支持的范围
        temperature=0.5,
        repetition_penalty=1.5
    )
    return pipe


def load_vector_db(embeddings):
    """加载向量数据库"""
    try:
        vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        return vector_db
    except Exception as e:
        print(f"加载向量数据库时出现错误: {e}")
        return None


def clear_gpu_memory():
    """清理显存"""
    torch.cuda.empty_cache()
    print("显存已清理")



def chat_with_rag(rag_chain):
    """多轮对话逻辑"""
    print("系统：您好！请问有什么可以帮您？（输入'exit'退出）")
    clear_gpu_memory()
    # todo : 合并时需修改
    # TempModel.query.delete()
    # db.session.commit()
    delete_all_records()

    while True:
        user_input = input("用户：")
        if user_input.lower() == 'exit':
            break

        print("Get response :", user_input)
        bef = time.time()

        try:
            # todo : 和其他部分合并时需要再次修改
            # memory = TempModel.query.filter_by().all()
            memory = get_all_records()
            history = []
            for question,answer in memory:
                print("question:",question)
                print("answer:",answer)
                history.append(HumanMessage(content=question))
                history.append(AIMessage(content=answer))
            
            result = rag_chain.invoke({
                "input": user_input,
                "chat_history": history,
            })
            ans = result["answer"].split("Assistant:")[-1].strip()
            # todo : 和其他部分合并时需要再次修改
            # db.session.add(TempModel(question=user_input, answer=ans))
            # db.session.commit()
            add_record(user_input, ans)

            print(result)
            print(f"系统：{ans}")
        except Exception as e:
            print(f"生成回答时出现错误: {e}")

        clear_gpu_memory()
        print("cost time:", time.time() - bef, "\n")


def main():
    # chat_with_rag(None)
    start = time.time()

    model_id = "Qwen/Qwen2-0.5B"
    # 加载模型和分词器
    model, tokenizer = load_model_and_tokenizer(model_id)

    # 创建推理管道
    pipe = create_inference_pipeline(model, tokenizer)
    print("time1:", time.time() - start, "\n")

    # 初始化大语言模型
    llm = HuggingFacePipeline(pipeline=pipe)

    embeddings = HuggingFaceEmbeddings(
        model_name='tbs17/MathBERT'
    )
    # 加载向量数据库
    vector_db = load_vector_db(embeddings)
    if vector_db is None:
        return
    print("time2:", time.time() - start, "\n")

    prompt_template = ChatPromptTemplate.from_template(
"""你是一个专业严谨的AI助手，**严格遵循以下规则**：
1. 仅使用提供的材料回答问题，不依赖外部知识
2. 回答需简洁准确，用1-3句完成且不重复
3. 无相关信息时直接说明"根据已知信息无法回答"
4. 始终使用简体中文

# 回答示例
Human: 1+1=?
Assistant: 1+1=2。

Human: 2+2=?
Assistant: 2+2=4。

# 可用材料
{context}

# 对话历史
{chat_history}

# 请回答接下来的问题
Human: {input}
Assistant:
""")

    # 构建历史感知链
    history_aware_retriever = create_history_aware_retriever(
        llm,
        vector_db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.5
            }  # 仅返回高相关性文档
        ),
        prompt=ChatPromptTemplate.from_messages([
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            ("human", "生成优化后的搜索查询："),
        ])
    )
    print("time3:", time.time() - start, "\n")

    rag_chain = create_retrieval_chain(
        history_aware_retriever,
        create_stuff_documents_chain(llm, prompt_template)
    )

    # 开始多轮对话
    chat_with_rag(rag_chain)


if __name__ == "__main__":
    main()
