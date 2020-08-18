import pymysql
from sshtunnel import SSHTunnelForwarder


class DataBaseHandle:
    ''' 定义一个 MySQL 操作类'''

    def __init__(self, host='127.0.01', username='xxx', password='xxx'
                 , database='xxx', port=10022):
        '''初始化数据库信息并创建数据库连接'''
        self.w_server = SSHTunnelForwarder(
            # 中间服务器地址
            ("xxx.64.47.xxx", 22),
            ssh_username="xxx",
            ssh_pkey="~/.ssh/id_rsa",
            # ssh_private_key_password="~/.ssh/id_rsa",
            # 目标的地址与端口，因为目标地址就是中间地址所以写127.0.0.1或者localhost
            remote_bind_address=('127.0.0.1', 3306),
            # 本地的地址与端口
            local_bind_address=('0.0.0.0', 10022)
        )
        # 启动ssh实例，后续的MySQL网络连接都将在这个环境下运行。
        self.w_server.start()
        # 后面开始对MySQL的数据进行初始化
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = pymysql.connect(host=self.host,
                                  user=self.username,
                                  password=self.password,
                                  database=self.database,
                                  port=self.port,
                                  charset='utf8')

    #  这里 注释连接的方法，是为了 实例化对象时，就创建连接。不许要单独处理连接了。
    #
    # def connDataBase(self):
    #     ''' 数据库连接 '''
    #
    #     self.db = pymysql.connect(self.host,self.username,self.password,self.port,self.database)
    #
    #     # self.cursor = self.db.cursor()
    #
    #     return self.db

    def insertDB(self, sql):
        ''' 插入数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def deleteDB(self, sql):
        ''' 操作数据库数据删除 '''
        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def updateDb(self, sql):
        ''' 更新数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def selectDb(self, sql):
        ''' 数据库查询 '''
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果

            data = self.cursor.fetchall()  # 返回所有记录列表

            print(data)

            # 结果遍历
            for row in data:
                sid = row[0]
                name = row[1]
                # 遍历打印结果
                print('sid = %s,  name = %s' % (sid, name))
        except:
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()

    def closeDb(self):
        ''' 数据库连接关闭 '''
        self.db.close()
        self.w_server.close()


if __name__ == '__main__':
    DbHandle = DataBaseHandle()
    DbHandle.selectDb('SELECT VERSION()')
    DbHandle.closeDb()