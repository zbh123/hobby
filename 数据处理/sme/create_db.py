import MySQLdb
from sshtunnel import SSHTunnelForwarder

with SSHTunnelForwarder(
        ("10.29.24.47", 222),  # ssh IP和port
        ssh_password="zts000000",  # ssh 密码
        ssh_username="tianyj",  # ssh账号
        remote_bind_address=("10.29.129.94", 3306)) as server:  # 数据库所在的IP和端口

    server.start()
    # 打印本地端口，已检查是否配置正确
    print(server.local_bind_port)

    conn = MySQLdb.connect(host="127.0.0.1",  # 固定写法
                           port=server.local_bind_port,
                           user="rpa",  # 数据库账号
                           passwd="zts000",  # 数据库密码
                           db='SME',
                           charset='utf8')  # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好表名


    print('连接成功')
    cur = conn.cursor()
    sql = """CREATE TABLE nsts_apply_list (
             index_1 CHAR(150),
             company CHAR(150),
             province CHAR(150),
             industry CHAR(150),
             name_bonders CHAR(150),
             project_leader_bonder CHAR(150),
             law_firm CHAR(150),
             lawyer	CHAR(150),
             account_firm CHAR(150),
             cpa CHAR(150),
             list_issue_ats	CHAR(150),
             audit_status CHAR(150),
             accept_date CHAR(150),
             one_feedback CHAR(150),
             one_reply CHAR(150),
             two_feedback CHAR(150),
             two_reply CHAR(150),
             three_feedback	CHAR(150),
             three_reply CHAR(150),
             four_feedback CHAR(150),
             four_reply	CHAR(150),
             five_feedback CHAR(150),
             five_reply	CHAR(150),
             six_feedback CHAR(150),
             six_reply CHAR(150),
             seven_feedback	CHAR(150),
             seven_reply CHAR(150),
             eight_feedback	CHAR(150),
             eight_reply CHAR(150),
             `current_time` CHAR(150)
)"""

    cur.execute(sql)
    print("CREATE TABLE OK")
    # 关闭数据库连接
    cur.close()
    # 关闭连接
    conn.close()