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
                           db='investment_banks',
                           charset='utf8')  # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好表名


    print('连接成功')
    cur = conn.cursor()
    sql = 'update csrc_ipo set data_time="2020-10-31" where `current_time`="2020-10-31"'
    # sql = """CREATE TABLE wind_star (
    #          code CHAR(150),
    #          bond_abbr CHAR(150),
    #          accept_date CHAR(150),
    #          fullname_issuer CHAR(150),
    #          accept_batch CHAR(150),
    #          audit_status CHAR(150),
    #          ipo_theme CHAR(150),
    #          ipo_theme_detail CHAR(150),
    #          list_standards CHAR(150),
    #          to_raise_funds	CHAR(150),
    #          sponsor_and_underwriter CHAR(150),
    #          account_firm CHAR(150),
    #          law_firm CHAR(150),
    #          asset_appraisal_agency CHAR(150),
    #          registration CHAR(150),
    #          csrc CHAR(150),
    #          update_time CHAR(150),
    #          `current_time` CHAR(150)
    #         )"""

    cur.execute(sql)
    print("CREATE TABLE OK")
    # 关闭数据库连接
    cur.close()
    # 关闭连接
    conn.close()



