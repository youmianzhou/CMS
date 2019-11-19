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

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
SECRET_KEY = 'x1x2x3x4x5x6'

