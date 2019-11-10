# encoding:utf-8
from flask import Blueprint, render_template, request, session, redirect, url_for
from db.mysqlConnection import *
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm
from flask import make_response
from utils.captcha import create_validate_code
from io import BytesIO
from datetime import timedelta


bp = Blueprint('admin', __name__, url_prefix= '/admin')


@bp.route('/login/', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('admin/login.html')

    else:
        form = LoginForm(request.form)
        if form.validate():
            online = request.form.get('online')
            captcha = request.form.get('captcha')
            if session.get('image').lower() != captcha.lower():
                return render_template('admin/login.html', message= '验证码不正确！')


            user = request.form.get('username')
            # 原始密码
            pwd = request.form.get('password')

            mysql = MyPymysqlPool("localdb")
            sql01 = """SELECT * FROM `jiaqicms`.`jq_user`  WHERE `username` = '{}' LIMIT 1""".format(user)

            sql01_data = mysql.getAll(sql01)

            if sql01_data:
                uid = sql01_data[0]['uid']
                username = str(sql01_data[0]['username'],encoding='utf-8')
                # 加密过后的密码
                password = str(sql01_data[0]['password'],encoding='utf-8')

                if username == user and check_password_hash(pwd, password):
                    session['user_id'] = uid
                    print('密码对！')
                    if online:  # 如果选择了记住我
                        session.permanent = True
                        bp.permanent_session_lifetime = timedelta(days=10)
                    return redirect(url_for('admin.index'))

                else:
                    error = '用户名或密码错误'
                    return render_template('admin/login.html', message = error)

            else:
                return render_template('admin/login.html', message = '别试了，没有此用户！')


@bp.route('/')
def index():
    return render_template('admin/index.html')

@bp.route('/code/')
def get_code():
    # 把strs发给前端，或者在后台使用session保存
    code_img, strs = create_validate_code()
    buf = BytesIO()
    code_img.save(buf, 'JPEG', quality = 70)
    buf_str = buf.getvalue()

    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    session['image'] = strs
    return response



