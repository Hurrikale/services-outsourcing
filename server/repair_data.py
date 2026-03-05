import json
import pymysql
import os
import sys
from typing import List, Dict

# 设置控制台输出编码为UTF-8
if sys.version_info[0] == 3:
    sys.stdout.reconfigure(encoding='utf-8')

def import_sql_file(file_path: str) -> None:
    """导入SQL文件"""
    try:
        sql_statement = None
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            # 将SQL文件按分号分割成单独的语句
            sql_statements = sql_content.split(';')
            for i in range(len(sql_statements)):
                statement = sql_statements[i].split("\'")
                if len(statement) > 1:
                    statement[1] = str(i+1)
                sql_statements[i] = "\'".join(statement)
            sql_statement = ";".join(sql_statements)
            print("here")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sql_statement)
        print(f"SQL文件 {file_path} 导入完成")
    except Exception as e:
        print(f"处理SQL文件 {file_path} 时出错: {str(e)}")

def get_file_type(file_path: str) -> str:
    """获取文件类型"""
    _, ext = os.path.splitext(file_path)
    return ext.lower()

def import_file(file_path: str) -> None:
    """根据文件类型选择相应的导入方法"""
    file_type = get_file_type(file_path)
    
    if file_type == '.sql':
        import_sql_file(file_path)
    else:
        print(f"不支持的文件类型: {file_type}")

def main():
    try:
        
        # 获取data目录下的所有文件
        data_dir = './data'
        files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
        
        for file_name in files:
            file_path = os.path.join(data_dir, file_name)
            print(f"正在导入 {file_path}...")
            import_file(file_path)
            print(f"{file_path} 导入完成")

    except Exception as e:
        print(f"导入过程中出错: {str(e)}")

if __name__ == "__main__":
    main()
    print("数据导入完成！")
