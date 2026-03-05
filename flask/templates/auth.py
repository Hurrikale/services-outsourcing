from flask import Blueprint, render_template, request, jsonify
from exts import mail
from flask_mail import Message
from random import randint


bp = Blueprint("auth", __name__ ,url_prefix="/auth")


@bp.route("/login")
def login():
    pass


@bp.route("/register")
def register():
    return render_template("register.html")


@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    captcha = randint(100000,999999)
    message = Message(subject=f"【数学解答系统】验证码 {captcha}", recipients=[email], body="此验证码仅用于邮箱身份验证，请勿泄漏与转发，如非本人操作，请忽略此短信。")
    mail.send(message)
    return jsonify({"code": 200,"message": "","data": None})


