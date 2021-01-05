import MySQLdb
from sshtunnel import SSHTunnelForwarder
import time

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
                           db='brokerage',
                           charset='utf8')  # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好表名
    print('连接成功')
    time.sleep(100)
    cur = conn.cursor()
    # sql = """CREATE TABLE shenzhen_month (
    #          month CHAR(150),
    #          total_amount CHAR(150),
    #          market_share CHAR(150),
    #          stock_trading_amount CHAR(150),
    #          fund_trading_amount CHAR(150),
    #          bond_trading_amount CHAR(150),
    #          warrants_trading_amount CHAR(150),
    #          `current_time` CHAR(150))"""

    # sql = """CREATE TABLE sse_month(
    #         member_name CHAR(150),
    #         number_seats CHAR(150),
    #         total CHAR(150),
    #         stock CHAR(150),
    #         investment_funds CHAR(150),
    #         ETF CHAR(150),
    #         treasury CHAR(150),
    #         amount_lgd CHAR(150),
    #         corporate_bonds CHAR(150),
    #         convertible_bonds CHAR(150),
    #         repurchase_bonds CHAR(150),
    #         warrants CHAR(150),
    #         current_month CHAR(150),
    #         `current_time` CHAR(150))
    #
    # """
    # sql = """CREATE TABLE shenzhen_total_day(
    # types_bond CHAR(150),
    # number CHAR(150),
    # transaction_amount CHAR(150),
    # turnover CHAR(150),
    # total_equity CHAR(150),
    # total_market_value CHAR(150),
    # negotiable_capital CHAR(150),
    # circulation_market_value CHAR(150),
    # `current_time` CHAR(150))"""
    # sql = """ CREATE TABLE sse_stock_day(
    # single_day_situation  CHAR(150),
    # stock CHAR(150),
    # mainboard_A CHAR(150),
    # mainboard_B CHAR(150),
    # ipo CHAR(150),
    # repurchase_bonds CHAR(150),
    # `current_time` CHAR(150)
    # )
    # """

    # sql = """CREATE TABLE sse_fund_day(
    # single_day_situation CHAR(150),
    # fund CHAR(150),
    # closed_fund CHAR(150),
    # ETF CHAR(150),
    # LOF CHAR(150),
    # trading_fund CHAR(150),
    # repurchase_fund CHAR(150),
    # `current_time` CHAR(150)
    # )
    # """
    # cur.execute(sql)
    print("CREATE TABLE OK")
    # 关闭数据库连接
    cur.close()
    # 关闭连接
    conn.close()
