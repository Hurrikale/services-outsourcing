import pymysql
from sqlalchemy import create_engine, text
from typing import List, Dict, Any
import config
from utils.logger import logger

class DatabaseManager:
    def __init__(self):
        self.vector_db = None
        self.connection_string = config.DB_URI
        self.engine = create_engine(self.connection_string)

    def init_vector_db(self, vector_db):  # 新增初始化方法
        """安全初始化向量数据库"""
        if not hasattr(vector_db, "as_retriever"):
            raise ValueError("无效的向量数据库对象")
        self.vector_db = vector_db
    
    def get_history(self, chat_id: int, limit: int = 3):
        try:
            with self.engine.connect() as conn:
                sql = text("""
                    SELECT id, question, answer, update_time
                    FROM question
                    WHERE chat_id = :chat_id
                    ORDER BY update_time DESC
                    LIMIT :limit
                """)
                
                query_params = {
                    "chat_id": chat_id,
                    "limit": limit
                }
                
                result = conn.execute(sql, query_params)
                contexts = [
                    (row[1],row[2])
                    for row in result
                ]
                
                return contexts
                
        except Exception as e:
            print(f"数据库查询错误: {str(e)}")
            return []

    def get_connection(self):
        """获取数据库连接"""
        return pymysql.connect(
            host=config.HOSTNAME,
            user=config.USERNAME,
            password=config.PASSWORD,
            database=config.DATABASE,
            charset='utf8mb4'
        )

    def search_similar_contexts(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """搜索相似的上下文（安全版本）"""
        try:
            # 添加类型检查
            if not self.vector_db or not hasattr(self.vector_db, "as_retriever"):
                raise RuntimeError("向量数据库未正确初始化")

            # 配置检索器
            retriever = self.vector_db.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": limit,
                    "score_threshold": 0.65  # 调整相似度阈值
                }
            )
            
            # 安全调用
            result = retriever.invoke(query)  # 修正参数格式
            # logger.info(f"检索结果的类型: {type(result)}")
            # for item in result:
            #    logger.info(f"单个结果的类型: {type(item)}, 内容: {item}")
            # 调试输出
            # logger.info(f"检索到{len(result)}条结果")

            return [{
                "content": doc.page_content,
                "metadata": doc.metadata
            } for doc in result if hasattr(doc, "page_content")]
            
        except Exception as e:
            logger.error(f"上下文检索失败: {str(e)}")
            return []

if __name__ == "__main__":
    # 测试数据库连接
    db = DatabaseManager()
    try:
        conn = db.get_connection()
        print("数据库连接成功！")
        conn.close()
    except Exception as e:
        print(f"数据库连接失败: {str(e)}")
