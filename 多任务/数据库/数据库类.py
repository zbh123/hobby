import pymysql


class ConnectSql():
    def __init__(self, host, user, passwd, dbName):
        self.host = host
        self.user = user
        self.passed = passwd
        self.dbName = dbName


    def connect(self):
        try:
            self.db = pymysql.connect(self.host, self.user, self.passed, self.dbName)
            self.cursor = self.db.cursor()
        except:
            print("数据库连接失败")
    def close(self):
        self.cursor.close()
        self.db.close()

    def get_db_info(self, sql):
        res = []
        try:
            self.connect()
            self.cursor.excute(sql)
            res = self.cursor.fetchone()
            self.close()
        except:
            res = "查询失败"
        return res
    def excute_db_command(self, sql):
        count = 0
        try:
            self.connect()
            self.cursor.excute(sql)
            self.db.commit()
            self.close()
        except:
            print("提交失败")
            self.db.rollback()


