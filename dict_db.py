"""
    连接数据库，
    数据库查询

"""
import pymysql


class Dictionary:
    def __init__(self):
        self.db = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database="dictionary",
            charset="utf8"
        )

    def cur(self):
        self.cur = self.db.cursor()

    def close(self):
        self.db.close()
        self.cur.close()

    def register(self, name, code):
        sql = "select name from user where name =%s;"
        self.cur.execute(sql, [name])
        r = self.cur.fetchone()
        if r:
            return False
        else:
            sql = "insert into user (name,passwd) values (%s,%s);"
            try:
                self.cur.execute(sql, [name, code])
                self.db.commit()
                return True
            except Exception as E:
                print(E)
                self.db.rollback()
                return False

    def login(self, name, code):
        sql = "select passwd from user where name =%s;"
        self.cur.execute(sql, [name])
        r = self.cur.fetchone()  # 返回值是一个列表
        if not r:
            return "count error"
        elif r[0] == code:
            return 'pass'
        else:
            return 'code error'

    def lookup(self, word):
        sql = "select `explain` from dictionary where word =%s "
        self.cur.execute(sql, [word])
        mean = self.cur.fetchone()
        if mean:
            return mean[0]
        else:
            return "can not find this word"

    def record_history(self, name, word):
        sql = "select id from user where name =%s;"
        self.cur.execute(sql, [name])
        name_id = self.cur.fetchone()
        sql = "insert into hist(word,user_id) values (%s,%s);"
        try:
            self.cur.execute(sql, [word, name_id])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def view_history(self):
        sql = "select top10.id,word,name,time from (select * from hist order by time desc limit 10)" \
              " as top10 left join user on top10.user_id=user.id;"
        self.cur.execute(sql)
        pieces = self.cur.fetchall()
        return pieces


if __name__ == "__main__":
    dic = Dictionary()
    dic.cur()
    for a, b, c, d in dic.view_history():
        print(f"序号{a}，单词{b},用户{c},时间{d}")
