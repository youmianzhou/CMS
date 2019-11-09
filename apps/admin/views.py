from flask import Blueprint

bp = Blueprint('admin', __name__)


@bp.route('/admin')
def index():
    return '这是后台首页'
