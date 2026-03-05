from flask import g, Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail,db
from flask_mail import Message
import random
import string
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


#/auth
bp = Blueprint("auth", __name__, url_prefix='/auth')


@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"code": 400, "message": "无效的请求数据"}), 400
            
        form = LoginForm(data=data)
        if form.validate():
            email = data.get('email')
            password = data.get('password')
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return jsonify({"code": 400, "message": "用户不存在"}), 400
            if not user.password:
                return jsonify({"code": 400, "message": "密码未设置"}), 400
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                return jsonify({"code": 200, "message": ""}), 200
            else:
                return jsonify({"code": 400, "message": "密码错误"}), 400
        else:
            print("表单验证错误:", form.errors)  # 添加错误信息打印
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            return jsonify({"code": 400, "message": " ".join(error_messages)}), 400
    except Exception as e:
        print(f"登录错误：{str(e)}")
        return jsonify({"code": 500, "message": "服务器错误"}), 500


@bp.route('/register',methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"code": 400, "message": "请求数据格式错误，应为 JSON 格式"}), 400
        
        print("接收到的完整注册数据:", data)  # 打印完整数据

        # 检查邮箱是否已注册
        if UserModel.query.filter_by(email=data.get('email')).first():
            return jsonify({"code": 400, "message": "该邮箱已被注册"}), 400
            
        # 验证验证码
        captcha = data.get('captcha')
        email = data.get('email')
        if not captcha or not email:
            return jsonify({"code": 400, "message": "验证码和邮箱不能为空"}), 400
            
        # 删除过期的验证码
        EmailCaptchaModel.query.filter(
            EmailCaptchaModel.email == email,
            EmailCaptchaModel.create_time < (datetime.now() - timedelta(minutes=5))
        ).delete()
        
        # 查询最新有效的验证码
        captcha_model = EmailCaptchaModel.query.filter_by(
            email=email,
            captcha=captcha
        ).order_by(EmailCaptchaModel.create_time.desc()).first()
        
        if not captcha_model:
            return jsonify({
                "code": 400,
                "message": "验证码错误或已过期"
            }), 400
            

        form = RegisterForm(data=data)

        if not form.validate():
            print("表单验证详细错误:", form.errors)  # 打印详细错误
            error_messages = []
            for errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"\n{error}")
            error_message_str = "".join(error_messages)
            return jsonify({"code": 400, "message": f"注册失败，原因：{error_message_str}"}), 400
        try:
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # 删除已使用的验证码
            db.session.delete(captcha_model)
            db.session.commit()
            return jsonify({"code": 200, "message": "注册成功，请登录"}), 200
        except Exception as e:
            print(f"注册错误：{str(e)}")
            return jsonify({"code": 500, "message": "服务器错误"}), 500

    except Exception as e:
        print(f"注册错误：{str(e)}")
        return jsonify({"code": 500, "message": "服务器错误"}), 500



@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/auth/login")


@bp.route("/captcha/email",methods=['POST'])
def get_email_captcha():
    print(g.start_time)
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({"code": 400, "message": "缺少邮箱参数", "data": None}), 400
        email = data['email']

        # 检查邮箱格式
        from email_validator import validate_email, EmailNotValidError
        try:
            validate_email(email)
        except EmailNotValidError:
            return jsonify({"code": 400, "message": "邮箱格式不正确"}), 400
        
        # 生成验证码
        captcha = "".join(random.choices(string.digits, k=6))
        
        message = Message(subject=f"【数学解答系统】验证码 {captcha}", recipients=[email], body="此验证码仅用于邮箱身份验证，有效期为5分钟，请勿泄漏与转发，如非本人操作，请忽略此邮件。")
        mail.send(message)
        email_captcha = EmailCaptchaModel(email=email, captcha=str(captcha))
        captcha_to_delete = EmailCaptchaModel.query.filter_by(email=email).first()
        db.session.add(email_captcha)
        db.session.commit()
        return jsonify({"code": 200,"message": "","data": None})
    except Exception as e:
        print(f"邮件发送错误: {str(e)}")
        return jsonify({"code": 500, "message": "服务器错误"}), 500




