# encoding:utf-8
import base64
from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from apps.admin.forms import LoginForm
from flask import make_response
from io import BytesIO
from datetime import timedelta
from .models import Users
from .decorators import login_required
import config
from utils.captcha import create_validate_code
from exts import db
from flask import jsonify



# 创建一个蓝图对象，蓝图已经注册得到app上了，所以蓝图对象相当于app
bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('admin/login.html')

    else:
        # print(session)
        form = LoginForm(request.form)
        # print(request.form)


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


@bp.route('/logout/')
@login_required
def logout():
    del session['user_id']
    return redirect(url_for('admin.login'))


# 个人信息页视图
@bp.route('/profile/')
# @login_required
def profile():
    # 根据session取得用户信息
    if config.ADMIN_USER_ID in session:
        user_id = session.get(config.ADMIN_USER_ID)
        # 2
        print(user_id)
        user = Users.query.get(user_id)  # 这是一个user对象
        # <Users 2>
        print(user)

        return render_template('admin/profile.html', user=user)


def checkpwd():
    oldpwd = request.args.get('oldpwd', '')
    if config.ADMIN_USER_ID in session:
        user_id = session.get(config.ADMIN_USER_ID)
        user = Users.query.filter_by(uid=user_id).first()

        if user.check_password(oldpwd):
            data = {
                'name': user.email,
                'status': 11
            }

        else:
            data = {
                'name': None,
                'status': 00
            }

        return jsonify(data)


#管理员修改密码
@bp.route('/editpwd/',methods=['GET', 'POST'])
@login_required
def editpwd():
    if request.method == 'GET':
        return render_template('admin/edit_pwd.html')
    else:
        oldpwd = request.form.get('oldpwd')
        newpwd1 = request.form.get('newpwd1')
        newpwd2 = request.form.get('newpwd2')
        print(oldpwd)
        user_id = session.get(config.ADMIN_USER_ID)
        user = Users.query.filter_by(uid=user_id).first()
        user.password = newpwd1
        db.session.commit()
        return render_template('admin/edit_pwd.html',message="密码修改成功！")
