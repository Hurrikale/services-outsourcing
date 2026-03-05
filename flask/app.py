from flask import Flask, render_template
from exts import mail
from flask_mail import Message
import config
from exts import mail
from templates.auth import bp as auth_bp


app = Flask(__name__)
app.config.from_object(config)

mail.init_app(app)


app.register_blueprint(auth_bp)