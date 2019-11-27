from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationships


class Users(db.Model):
    __tablename__ = 'jq_user'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result


# 定义文章分类开始
class Articles_Cat(db.Model):

    __tablename__ = 'jq_article_category'
    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 分类ID
    parent_id = db.Column(db.Integer, nullable=False)  # 分类父ID,父ID不能为空
    cat_name = db.Column(db.String(20), nullable=False)  # 栏目名称
    keywords = db.Column(db.String(20), nullable=False)  # 栏目关键字
    description = db.Column(db.String(200), nullable=True)  # 栏目描述可以为空
    cat_sort = db.Column(db.Integer, nullable=True)  # 栏目排序
    # template=db.Column(db.String(80),nullable=False)# 栏目模板
    status = db.Column(db.Integer, nullable=False)  # 显示还是隐藏
    dir = db.Column(db.String(80), nullable=False)  # 如果实现静态化，该栏目的保存路径
    # articles = db.relationship("Articles", lazy="dynamic")  # 一个栏目对应多个文章
