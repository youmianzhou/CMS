# encoding:utf-8
import base64
from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm
from flask import make_response
from utils.captcha import create_validate_code
from io import BytesIO
from datetime import timedelta
from .models import Users
from .decorators import login_required
import config

# 创建一个蓝图对象，蓝图已经注册得到app上了，所以蓝图对象相当于app
bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('admin/login.html')

    else:
        form = LoginForm(request.form)
        print(request.form)
        print(session)

        if form.validate():
            user = request.form.get('username')
            pwd = request.form.get('password')
            online = request.form.get('online')
            captcha = request.form.get('captcha')

            if session.get('image').lower() != captcha.lower():
                return render_template('admin/login.html', message='验证码不正确！')

            else:

                users = Users.query.filter_by(username=user).first()
                if users:
                    if user == users.username and users.check_password(pwd):
                        session[config.ADMIN_USER_ID] = users.uid
                        print('密码对！')
                        if online:  # 如果选择了记住我
                            session.permanent = True
                            bp.permanent_session_lifetime = timedelta(days=10)
                        return redirect(url_for('admin.index'))

                    else:
                        error = '用户名或密码错误'
                        return render_template('admin/login.html', message=error)

                else:
                    return render_template('admin/login.html', message='别试了，没有此用户！')

        else:
            return render_template('admin/login.html', message=form.errors)


@bp.route('/')
def index():
    return render_template('admin/index.html')


@bp.route('/code/')
def get_code():
    # 把strs发给前端，或者在后台使用session保存
    code_img, strs = create_validate_code()
    buf = BytesIO()
    code_img.save(buf, 'JPEG', quality=70)
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    session['image'] = strs

    return response


# @bp.before_request
# def before_request():
#     if config.ADMIN_USER_ID in session:
#         user_id = session.get(config.ADMIN_USER_ID)
#         user = Users.query.get(user_id)
#         if user:
#             g.admin_user = user.username


# @bp.route('/test/')
# @login_required
# def test():
#     return 'test index'


# @bp.route('/logout/')
# @login_required
# def logout():
#     del session['user_id']
#     return redirect(url_for('admin.login'))
