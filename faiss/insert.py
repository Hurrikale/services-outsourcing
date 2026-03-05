import sqlite3
import os

db_path = r'/home/hurrikale/Desktop/ServiceOutsourcing/database/questions.db'
data_dir = r'/home/hurrikale/Desktop/ServiceOutsourcing/data/data'

os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''DROP TABLE talks''')

c.execute('''CREATE TABLE IF NOT EXISTS catalog
             (userid INT NOT NULL , talkid INT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS categorization
             (type TEXT NOT NULL , tag TEXT)''')

c.execute('''CREATE TABLE talks
             (answer TEXT , question TEXT NOT NULL , talkid INT NOT NULL , tag TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS users
             (userid INT NOT NULL , name TEXT NOT NULL , password TEXT NOT NULL)''')

conn.commit()

files = os.listdir(data_dir)
now = 0

for file_name in files:
    file_path = os.path.join(data_dir, file_name)
    with open(file_path, 'r') as file:
        content = file.readlines()[1:-1]
        for j in range(1, len(content), 4):
            problem = content[j][20:-3].strip()
            solution = content[j+1][21:-2].strip()
            now -= 1
            # 使用参数化查询
            sql = "INSERT INTO talks (answer, question, talkid, tag) VALUES (?, ?, ?, ?)"
            c.execute(sql, (solution, problem, now, None))

conn.commit()
conn.close()