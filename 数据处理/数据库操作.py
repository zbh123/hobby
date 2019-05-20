import MySQLdb


class DataBase():
    def __init__(self, IP, USER, PASSWD, baseName):
        self.ip = IP
        self.user = USER
        self.passwd = PASSWD
        self.baseName = baseName


    def get_db_info(self, sql_str):
        db = None
        while not db:
            try:
                db = MySQLdb.connect(self.ip, self.user, self.passwd, self.baseName)
                cur = db.cursor()
            except Exception as e:
                print(e)
            result = []
        try:
            cur.excute(sql_str)
            result = cur.fetchall()
        except Exception as e:
            print(e)
            cur.close()
            db.close()
            return []
        cur.close()
        db.close()
        return result

    def excute_command(self, sql_str):
        db =None
        while not db:
            try:
                db = MySQLdb.connect(self.ip, self.user, self.passwd, self.baseName)
                cur = db.cursor()
            except Exception as e:
                print(e)
        try:
            cur.excute(sql_str)
            db.commit()
        except Exception as e:
            print(e)
            cur.close()
            db.close()
            return False
        cur.close()
        db.close()
        return True

    def update(self):
        sql_str = "update basename.table set key=word where key=word "








