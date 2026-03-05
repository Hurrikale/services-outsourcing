from functools import wraps
from flask import g, redirect, url_for, flash

def login_required(func):
    #保留func的信息
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            flash("请先登录！", 'error')
            return redirect(url_for('auth.login'))
    return inner

