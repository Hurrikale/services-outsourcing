import wtforms
from pyexpat.errors import messages
from models import UserModel, EmailCaptchaModel
from exts import db
from wtforms.validators import Length, Email, Length, EqualTo, InputRequired


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField()
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])
    
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")
        
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        if len(captcha) != 6:
            raise wtforms.ValidationError(message="验证码错误！")
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="验证码错误！")
        else: # todo : 性能优化
            db.session.delete(captcha_model)
            db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators= [Length(min=3, max=100, message="标题格式错误！")])
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误！")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误！")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题id!")])