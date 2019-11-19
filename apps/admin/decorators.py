# -*- coding:utf-8 -*-
from functools import wraps
from flask import session,redirect,url_for,request
from .models import Users,Auth,Role
import config
#登录限制装饰器
def login_required(func):
     @wraps(func)
     def wrapper(*args, **kwargs):
         if session.get(config.ADMIN_USER_ID):
             return func(*args, **kwargs)
         else:
             return redirect(url_for('admin.login'))
     return wrapper
# 有无访问权限装饰器： 判断用户权限控制
def admin_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get(config.ADMIN_USER_ID)
        admin = Users.query.join(
            Role
        ).filter(
            Role.id == Users.role_id,
            Users.uid == user_id
        ).first()
        auths = admin.jq_role.auths  # 将原本存储的权限字符串转换为列表
        auths_list1 = auths.split(",")
        auths_list2 = []
        for i, val in enumerate(auths_list1):
            auths_list2.append(int(val))
        auths_list3 = []
        auth_list = Auth.query.all()
        for i in auth_list:
            for v in auths_list2:
                if v == i.id:
                    auths_list3.append(i.url)
        rule = str(request.url_rule)
        if rule not in auths_list3:
            return "对不起，您无权访问，您拥有的权限为{}, 现在访问的为{}".format(auths_list3, rule)
        # else:
        #     print("可以访问")
            # return redirect(url_for('admin.index'))
        return func(*args, **kwargs)
    return wrapper
