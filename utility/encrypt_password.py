from werkzeug.security import generate_password_hash, check_password_hash
from db.mysqlConnection import *
import traceback

class Encrypt_Password():
    # def __init__(self, raw_password):
    #     self.raw_password = raw_password

    # 获取加密后密码
    @property
    def password(self):
        return self._password

    # 设置密码
    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)  # 密码加密

    # 检查密码
    def check_password(self, raw_password):
        result = check_password_hash(self._password, raw_password)
        return result


class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value


if __name__ == '__main__':
    # s = Student()
    # s.score = 60  # OK，实际转化为s.set_score(60)
    # print(s.score)  # OK，实际转化为s.get_score()
    #
    # s.score = 9999
    # print(s.score)

    ep = Encrypt_Password()
    # ep.password= '123456'
    # print(ep.password)
    #
    # result = ep.check_password('123456')
    # print(result)
    mysql = MyPymysqlPool("localdb")

    sql01 = """SELECT uid,`password` FROM `jiaqicms`.`jq_user`  WHERE `username` = 'admin'"""
    sql01_data = mysql.getAll(sql01)

    for data in sql01_data:
        uid = data['uid']
        pw = str(data['password'], encoding='utf-8')
        ep.password = pw
        # print(type(ep.password))

        sql02 = """UPDATE `jiaqicms`.`jq_user` SET `password` = '{}' WHERE uid = {} """.format(str(ep.password), uid)
        print(sql02)
        mysql.update(sql02)

    mysql.dispose()



