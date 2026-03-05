import faiss
from sentence_transformers import SentenceTransformer
import sqlite3
import os
import time
import numpy as np

db_path = r'/home/hurrikale/Desktop/ServiceOutsourcing/database/questions.db'
data_dir = r'/home/hurrikale/Desktop/ServiceOutsourcing/data/data'
input_path=r'cache.npy'

os.makedirs(os.path.dirname(db_path), exist_ok=True)

start = time.time()

conn = sqlite3.connect(db_path)
c = conn.cursor()

# 1. 生成文本向量
model = SentenceTransformer('tbs17/MathBERT')

print("time1:",time.time() - start,"\n")

texts = []
questions = c.execute("SELECT question from talks")
for i in questions:
    texts.append(i[0])
# texts = ["sample1","sample2","sample3"]

print("time2:",time.time() - start,"\n")

embeddings = np.load(input_path)
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)  # 精确搜索
index.add(embeddings)

print("time4:",time.time() - start,"\n")

# 2. 搜索相似文本
query = "What is $35.2 + 49.3$?"
query_embedding = model.encode([query])
distances, indices = index.search(query_embedding, k=10)

# 3. 输出结果
print("最相似的文本：")
for idx in range(len(indices[0])):
    print(f"- {texts[indices[0][idx]]} (距离: {distances[0][idx]:.4f})")

print("time5:",time.time() - start,"\n")