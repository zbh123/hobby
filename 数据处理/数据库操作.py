import MySQLdb
'''
left join on简介,首先确认要选取的内容即主框架select * from result where id=10， 其中left join左边的是基础库表，
右边的是选取元素的库表，on 之后=左边的是基础库表的内容，即根据主框架能得到的数据，右边的是对应库表的内容，两者是同一性质在不能库表的体现
然后，left join 。。。 on 可以多次使用
select job.job_name, job.buildname, test.testname, test.id, starttime, endtime from result 
left join job on result.id = job.id left join test on result.test_id = test.id where result.id=10
'''

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








