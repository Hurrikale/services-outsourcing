import mysql.connector
import torch
import psutil
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_documents_from_db(mydb, table_name):
    mycursor = mydb.cursor()
    query = f"SELECT * FROM {table_name}"
    mycursor.execute(query)
    results = mycursor.fetchall()
    documents = []
    for row in results:
        content = row[1]
        doc = Document(page_content=content, metadata={})
        documents.append(doc)
    return documents

try:
    # 连接到 MySQL 数据库
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="F0r_5ErV1<E_0u7s0ur<1n6",
        database="mydatabase"
    )

    documents = []
    documents.extend(load_documents_from_db(mydb, "context"))

    # 关闭数据库连接
    mydb.close()

    # 文本分块（chunk_size需与嵌入模型匹配）
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "！", "？"]
    )
    chunks = text_splitter.split_documents(documents)

    # 查看初始内存占用
    print(f"初始内存占用: {psutil.virtual_memory().used / (1024 * 1024):.2f} MB")

    device = "cuda" if torch.cuda.is_available() else "cpu"

    embeddings = HuggingFaceEmbeddings(
    model_name="Qwen/Qwen2.5-3B-Instruct",
    model_kwargs={"trust_remote_code": True, "device": device}
    )

    # 查看加载模型后的内存占用
    print(f"加载模型后内存占用: {psutil.virtual_memory().used / (1024 * 1024):.2f} MB")

    # 创建FAISS向量数据库
    vector_db = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    # 保存索引（可选）
    vector_db.save_local("faiss_index")
    print("保存成功！")

except mysql.connector.Error as err:
    print(f"数据库连接错误: {err}")
except Exception as e:
    print(f"发生未知错误: {e}")
