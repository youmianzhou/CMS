import redis

# 调试模式
DEBUG = True
DB_USERNAME = 'root'
DB_PASSWORD = '83810204'
DB_HOST = '127.0.0.1'
DB_POST = '3306'
DB_NAME = 'jiaqicms'
DB_URI = 'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{db}?charset-utf8'.format(username=DB_USERNAME,
                                                                                               password=DB_PASSWORD,
                                                                                               host=DB_HOST,
                                                                                               port=DB_POST,
                                                                                               db=DB_NAME)

# 数据库链接
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

ADMIN_USER_ID = 'HEBOANHEHE'
# CSRF_ENABLED = True

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# 配置session参数,用redis来保存session
SESSION_TYPE = 'redis'
SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,
                                  port=REDIS_PORT)

# session秘钥
SECRET_KEY = 'x1x2x3x4x5x6x7x8x9x0'
# 是否使用secret_key签名session_data
SESSION_USE_SIGNER = True
# 设置session的过期时间
PERMANENT_SESSION_LIFETIME = 3600 * 24
