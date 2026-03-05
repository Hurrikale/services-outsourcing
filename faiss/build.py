from sentence_transformers import SentenceTransformer
import sqlite3
import os
import time
import numpy as np

db_path = r'/home/hurrikale/Desktop/ServiceOutsourcing/database/questions.db'
data_dir = r'/home/hurrikale/Desktop/ServiceOutsourcing/data/data'
output_path=r'cache'

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

embeddings = model.encode(texts)

conn.close()

print("time3:",time.time() - start,"\n")

# 2. 存入文件
np.save(output_path, embeddings)

print("time4:",time.time() - start,"\n")