from datetime import datetime, timedelta
from sqlalchemy import func  # 添加这行导入

from exts import db


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # 修改字段名
    email = db.Column(db.String(100), nullable=True)  # 修改为可为空
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username=None, email=None, password=None, **kwargs):
        super(UserModel, self).__init__(**kwargs)
        if username:
            self.username = username
        if email:
            self.email = email
        if password:
            self.password = password  # 修改字段名

class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    def is_expired(self, expire_minutes=5):
        return datetime.now() > self.create_time + timedelta(minutes=expire_minutes)

class ChatModel(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chatname = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    author = db.relationship('UserModel', backref='chats')
    questions = db.relationship('QuestionModel', back_populates='chat', overlaps="questions")  

class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    update_time = db.Column(db.DateTime, default=func.now())

    # 外键
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # 关系
    chat = db.relationship('ChatModel', back_populates='questions', overlaps="questions")  
    author = db.relationship('UserModel', backref='questions')
