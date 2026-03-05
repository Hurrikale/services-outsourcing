"""
Main Flask application for chat service with authentication and RAG integration.
"""

import time
import os
import logging
import json
from logging.handlers import RotatingFileHandler
import asyncio
import threading

from flask import Flask, g, session, render_template, request, jsonify, redirect, url_for
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import text
import urllib.parse

import config
from exts import db, mail
from models import UserModel, QuestionModel, ChatModel
from decorators import login_required
from utils.logger import logger

# Constants
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = 'logs/app.log'
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

class ChatApplication:
    """Main application class encapsulating Flask app and chat functionality."""
    rag_engine = None
    init_lock = threading.Lock()  # 初始化锁，确保线程安全
    is_initializing = False  # 初始化状态标志
    
    def __init__(self):
        self.app = Flask(__name__)
        self.rag_engine = None
        self._configure_app()
        self._initialize_extensions()
        self._setup_routes()
        # 启动后台初始化线程
        threading.Thread(
            target=asyncio.run, 
            args=(self._first_init_rag_engine(),),
            daemon=True
        ).start()
        
    def _configure_app(self):
        """Configure Flask application settings."""
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
        self.app.config.from_object(config)
        self.app.before_request(self._my_before_request)
        self.app.after_request(self._log_response_info)
        self.app.context_processor(self._my_context_processor)
        
    def _initialize_extensions(self):
        """Initialize Flask extensions."""
        db.init_app(self.app)
        mail.init_app(self.app)
        CSRFProtect(self.app)
        Migrate(self.app, db)

    def _init_rag_engine(self):
        """Initialize the RAG engine with concurrency control."""
        # 使用锁确保同一时间只有一个线程能执行初始化
        with self.init_lock:
            # 检查是否正在初始化或已初始化
            if self.is_initializing:
                logger.info("Another initialization is in progress, waiting...")
                # 等待当前初始化完成
                while self.is_initializing:
                    time.sleep(0.1)  # 短暂休眠避免CPU占用过高
                    
            if self.rag_engine is None:
                try:
                    self.is_initializing = True  # 设置初始化中标志
                    logger.info("Initializing RAG engine")
                    from rag_model.rag_engine import RAGEngine
                    self.rag_engine = RAGEngine()
                    if not self.rag_engine.is_ready():
                        logger.info("开始加载模型...")
                        if not self.rag_engine.load_model():
                            logger.error("模型加载失败")
                            return False
                        if not self.rag_engine.is_ready():
                            logger.error("模型加载后仍未就绪")
                            return False
                    logger.info("RAG 引擎初始化成功")
                    return True
                finally:
                    self.is_initializing = False  # 无论是否成功，都清除初始化标志
        return True
        
    async def _first_init_rag_engine(self):
        if not self._init_rag_engine():
            logger.error(f"RAG engine initialization failed")
    
    def _setup_routes(self):
        """Set up application routes."""
        self.app.add_url_rule('/', view_func=self._home)
        self.app.add_url_rule('/index', view_func=self._index, methods=['GET'])
        self.app.add_url_rule('/chat/new', view_func=self._newchat, methods=['POST'])
        self.app.add_url_rule('/sendmessage', view_func=self._sendmessage, methods=['POST'])
        self.app.add_url_rule('/rename', view_func=self._rename, methods=['POST'])
        self.app.add_url_rule('/delete', view_func=self._delete, methods=['POST'])
        self.app.add_url_rule('/firstquery', view_func=self._firstquery, methods=['POST'])
        self.app.add_url_rule('/api', view_func=self._api, methods=['GET'])
    
    # 注册蓝图
    def register_blueprint(self, blueprint):
        self.app.register_blueprint(blueprint)

    # Route handlers
    @login_required
    def _home(self):
        """Redirect to login page."""
        return redirect(url_for('auth.login'))
    
    @login_required
    def _index(self):
        """Render the main index page."""
        return render_template("index.html")
    
    @login_required
    def _newchat(self):
        """Create a new chat session."""
        logger.info("收到 chat/new 请求")
        try:
            data = request.get_json()
            user_id = session.get("user_id")
            logger.info(f"当前会话信息: {dict(session)}")
            user = UserModel.query.get(user_id)

            # 检查用户是否存在
            if not user:
                logger.error(f"用户 {user_id} 不存在")
                return jsonify({"code": 400, "message": "用户不存在"}), 400
            
            logger.info(f"请求数据: {data}")
            if not data or 'name' not in data:
                logger.error("缺少必要参数")
                return jsonify({"code": 400, "message": "缺少必要参数"}), 400

            logger.info(f"创建新聊天: {data['name']}")

            num = ChatModel.query.filter_by(author_id=user_id).count() + 1
            chat = ChatModel(chatname=data['name']+f"{num}", author_id=user_id)
            db.session.add(chat)
            db.session.commit()

            logger.info(f"聊天创建成功，ID: {chat.id}")
            return jsonify({"code": 200, "id": chat.id, "number": f"{num}"}), 200
        except Exception as e:
            logger.error(f"创建聊天失败: {str(e)}", exc_info=True)
            db.session.rollback()
            return jsonify({"code": 400, "message": f"出错原因：{e}"}), 400
    
    @login_required
    def _sendmessage(self):
        """Handle sending a message and getting a response."""
        try:
            data = request.get_json()
            if not data:
                logger.error("请求数据为空")
                return jsonify({"code": 400, "message": "请求数据为空"}), 400
                
            if 'question' not in data:
                logger.error("缺少问题参数")
                return jsonify({"code": 400, "message": "缺少问题参数"}), 400
                
            if 'chat_id' not in data:
                logger.error("缺少聊天ID参数")
                return jsonify({"code": 400, "message": "缺少聊天ID参数"}), 400

            user_id = session.get("user_id")
            question = data['question']
            chat_id = data['chat_id']
            
            logger.info(f"收到问题: {question}, chat_id: {chat_id}")

            # 初始化 RAG 引擎
            logger.info("开始初始化 RAG 引擎")
            if not self._init_rag_engine():
                logger.error("RAG 引擎初始化失败")
                return jsonify({"code": 500, "message": "RAG 引擎初始化失败"}), 500

            # 检查 RAG 引擎状态
            if not self.rag_engine.is_ready():
                logger.error("RAG 引擎未准备就绪")
                return jsonify({"code": 500, "message": "RAG 引擎未准备就绪"}), 500

            # 生成答案
            logger.info("开始生成答案")
            try:
                answer = self.rag_engine.generate_answer(question, int(chat_id))
                logger.info("答案生成完成")
            except Exception as e:
                logger.error(f"生成答案失败: {str(e)}", exc_info=True)
                return jsonify({"code": 500, "message": f"生成答案失败: {str(e)}"}), 500

            # 保存到数据库
            try:
                question_record = QuestionModel(
                    question=question,
                    answer=answer,
                    chat_id=chat_id,
                    author_id=user_id
                )
                db.session.add(question_record)
                result = db.session.execute(
                    text("UPDATE chat SET update_time = CURRENT_TIMESTAMP WHERE id = :chat_id"),
                    {"chat_id": chat_id}
                )
                print(f"受影响的行数: {result.rowcount}")
                db.session.commit()
                logger.info(f"问答记录保存成功，ID: {question_record.id}")
            except Exception as e:
                logger.error(f"保存问答记录失败: {str(e)}", exc_info=True)
                db.session.rollback()

            return jsonify({
                "code": 200,
                "result": answer
            }), 200
            
        except Exception as e:
            logger.error(f"处理问题失败: {str(e)}", exc_info=True)
            return jsonify({
                "code": 500,
                "message": f"处理失败: {str(e)}"
            }), 500
        
    def _api(self):
        """For Test"""
        logger.info("收到测试")
        try:
            # 从URL查询字符串中获取question参数
            question = request.args.get('question')
            # 先进行URL解码（处理%2B等编码字符）
            question = urllib.parse.unquote(question)
            
            if not question:
                logger.error("缺少问题参数")
                return jsonify({"code": 400, "message": "缺少问题参数"}), 400
            
            logger.info(f"收到问题: {question}")

            # 初始化 RAG 引擎
            logger.info("开始初始化 RAG 引擎")
            if not self._init_rag_engine():
                logger.error("RAG 引擎初始化失败")
                return jsonify({"code": 500, "message": "RAG 引擎初始化失败"}), 500

            # 检查 RAG 引擎状态
            if not self.rag_engine.is_ready():
                logger.error("RAG 引擎未准备就绪")
                return jsonify({"code": 500, "message": "RAG 引擎未准备就绪"}), 500

            # 生成答案
            logger.info("开始生成答案")
            try:
                answer = self.rag_engine.generate_answer(question, -1)
                logger.info("答案生成完成")
            except Exception as e:
                logger.error(f"生成答案失败: {str(e)}", exc_info=True)
                return jsonify({"code": 500, "message": f"生成答案失败: {str(e)}"}), 500

            return jsonify({
                "code": 200,
                "result": answer
            }), 200
            
        except Exception as e:
            logger.error(f"处理问题失败: {str(e)}", exc_info=True)
            return jsonify({
                "code": 500,
                "message": f"处理失败: {str(e)}"
            }), 500

    
    @login_required
    def _rename(self):
        """Rename a chat session."""
        data = request.get_json()
        try:
            chat = ChatModel.query.get(data['currentChatId'])
            if chat is None:
                return jsonify({"code": 404, "message": "要修改的聊天记录不存在"}), 404
            chat.chatname = data['newName']
            db.session.commit()
            return jsonify({"code": 200, "message": ""}), 200
        except Exception as e:
            return jsonify({"code": 400, "message": f"出错原因：{e}"}), 400
    
    @login_required
    def _delete(self):
        """Delete a chat session."""
        data = request.get_json()
        try:
            to_delete = ChatModel.query.filter_by(id=data['currentChatId']).first()
            if to_delete is None:
                return jsonify({"code": 404, "message": "要删除的聊天记录不存在"}), 404
            QuestionModel.query.filter_by(chat_id=to_delete.id).delete()
            db.session.delete(to_delete)
            db.session.commit()
            return jsonify({"code": 200, "message": ""}), 200
        except Exception as e:
            return jsonify({"code": 400, "message": f"出错原因：{e}"}), 400
    
    @login_required
    def _firstquery(self):
        """Get initial chat history for a user."""
        try:
            user_id = session.get("user_id")
            chats = ChatModel.query.filter_by(author_id=user_id).order_by(ChatModel.update_time.desc())
            result = []
            for chat in chats:
                mess = [{ "sender": 'AI', "message": '你好！有什么我可以帮助的吗？' }]
                for quest in chat.questions:
                    mess.append({ "sender": 'user', "message": quest.question })
                    mess.append({ "sender": 'AI', "message": quest.answer })
                
                result.append({
                        'id': chat.id,
                        'time': int(time.mktime(chat.update_time.timetuple())),
                        'name': chat.chatname,
                        'messages': mess,
                        'date': None
                    })
            
            # 返回 JSON 格式的聊天记录数据
            return jsonify({'code': 200, 'result': result}), 200
        except Exception as e:
            # 若出现异常，返回错误信息
            return jsonify({'code': 500, 'error': str(e)}), 500
    
    def _my_before_request(self):
        """Before request hook for setting user and logging request info."""
        user_id = session.get("user_id")
        if user_id:
            try:
                user = db.session.get(UserModel, user_id)
                setattr(g, 'user', user)
            except Exception as e:
                logger.error(f"获取用户信息失败: {str(e)}")
                setattr(g, 'user', None)
        else:
            setattr(g, 'user', None)
        
        """记录请求信息"""
        start_time = time.time()
        g.start_time = start_time
        
        # 获取请求信息
        request_info = {
            'method': request.method,
            'url': request.url,
            'headers': dict(request.headers),
            'args': dict(request.args),
            'form': dict(request.form),
            'json': request.get_json(silent=True) or {}
        }
        
        # 记录请求信息
        logger.info(f"\n{'='*50}\n请求信息:")
        logger.info(f"方法: {request.method}")
        logger.info(f"URL: {request.url}")
        logger.info(f"参数: {json.dumps(request_info['args'], ensure_ascii=False)}")
        logger.info(f"表单数据: {json.dumps(request_info['form'], ensure_ascii=False)}")
        logger.info(f"JSON数据: {json.dumps(request_info['json'], ensure_ascii=False)}")
    
    def _log_response_info(self, response):
        """After request hook for logging response info."""
        # 计算响应时间
        end_time = time.time()
        duration = end_time - g.start_time
        
        # 获取响应信息
        response_info = {
            'status_code': response.status_code,
            'duration': f"{duration:.2f}秒",
            'headers': dict(response.headers)
        }
        
        # 记录响应信息
        logger.info(f"\n响应信息:")
        logger.info(f"状态码: {response.status_code}")
        logger.info(f"响应时间: {duration:.2f}秒")
        logger.info(f"{'='*50}\n")
        
        return response
    
    def _my_context_processor(self):
        """Context processor to make user available in templates."""
        return {"user": g.user}


def setup_logging():
    """Configure application logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # File handler
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_SIZE,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def create_app():
    """Application factory function."""
    setup_logging()
    app = ChatApplication()
    # 注册蓝图（由于原始代码中注释了qa_bp，这里只注册auth_bp）
    from blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    # from blueprints.qa import bp as qa_bp
    # app.register_blueprint(qa_bp)
    return app.app

# Create and run application
app = create_app()

if __name__ == '__main__':
    # Configure production settings
    os.environ['FLASK_ENV'] = 'production'
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True,
        use_reloader=False
    )
