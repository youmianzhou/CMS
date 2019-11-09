from flask import Blueprint

bp = Blueprint('common', __name__)


@bp.route('/common')
def index():
    return '这是公共部分首页'