import json
import pymysql
import os
import sys
from typing import List, Dict

# 设置控制台输出编码为UTF-8
if sys.version_info[0] == 3:
    sys.stdout.reconfigure(encoding='utf-8')

def create_table_if_not_exists(cursor) -> None:
    """创建表（如果不存在）"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS context (
        id INT AUTO_INCREMENT PRIMARY KEY,
        content TEXT NOT NULL,
        tags VARCHAR(255)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    """
    cursor.execute(create_table_sql)

def insert_qa_pair(cursor, question: str, analysis: str) -> None:
    """插入问答对到数据库"""
    content = f"问题：{question}\n\n解答：{analysis}"
    tags = "数学"  # 可以根据内容分析添加更多标签
    
    insert_sql = """
    INSERT INTO context (content, tags)
    VALUES (%s, %s)
    """
    cursor.execute(insert_sql, (content, tags))

def import_json_file(file_path: str, connection) -> None:
    """导入JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    if 'question' in data and 'analysis' in data:
                        with connection.cursor() as cursor:
                            insert_qa_pair(cursor, data['question'], data['analysis'])
                    connection.commit()
                except json.JSONDecodeError:
                    print(f"跳过无效的JSON行: {line[:100]}...")
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")

def import_sql_file(file_path: str, connection) -> None:
    """导入SQL文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            with connection.cursor() as cursor:
                # 将SQL文件按分号分割成单独的语句
                sql_statements = sql_content.split(';')
                for statement in sql_statements:
                    statement = statement.strip()
                    if statement and statement.startswith('INSERT'):
                        try:
                            # 修改为INSERT IGNORE跳过重复记录
                            statement = statement.replace('INSERT INTO', 'INSERT IGNORE INTO')
                            cursor.execute(statement)
                            connection.commit()
                        except Exception as e:
                            print(f"执行SQL语句时出错: {str(e)}")
                            print(f"问题语句: {statement[:200]}...")
                            continue
        print(f"SQL文件 {file_path} 导入完成")
    except Exception as e:
        print(f"处理SQL文件 {file_path} 时出错: {str(e)}")

def get_file_type(file_path: str) -> str:
    """获取文件类型"""
    _, ext = os.path.splitext(file_path)
    return ext.lower()

def import_file(file_path: str, connection) -> None:
    """根据文件类型选择相应的导入方法"""
    file_type = get_file_type(file_path)
    
    if file_type == '.json':
        import_json_file(file_path, connection)
    elif file_type == '.sql':
        import_sql_file(file_path, connection)
    else:
        print(f"不支持的文件类型: {file_type}")

def main():
    # 数据库连接配置
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='F0r_5ErV1<E_0u7s0ur<1n6',
        database='mydatabase',
        charset='utf8mb4'
    )

    try:
        # 创建表
        with connection.cursor() as cursor:
            create_table_if_not_exists(cursor)
        
        # 获取data目录下的所有文件
        data_dir = './data'
        files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
        
        for file_name in files:
            file_path = os.path.join(data_dir, file_name)
            print(f"正在导入 {file_path}...")
            import_file(file_path, connection)
            print(f"{file_path} 导入完成")

    except Exception as e:
        print(f"导入过程中出错: {str(e)}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
    print("数据导入完成！")
