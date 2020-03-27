from flask import Flask, render_template, request, redirect, url_for, session
import logging
import sqlite3
import time
import os
from collections import OrderedDict

#设置templates
app = Flask(__name__, template_folder='./templates')
#设置秘钥，session时用
app.config["SECRET_KEY"] = '123456'
script_path = os.path.dirname(os.path.abspath(__file__))
log = logging.basicConfig(level=logging.DEBUG, filename='test.log',
                          format='%(asctime)s,%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                          datefmt='%a, %d %b %Y %H:%M:%S')
sqlite_path = os.path.join(script_path, 'lock.db')

def get_sql_info(sql):
    db = None
    while not db:
        try:
            db = sqlite3.connect(sqlite_path)
            cur = db.cursor()
        except:
            log('Connect sqlite error')

    res = []
    try:
        cur.execute(sql)
        res = cur.fetchall()
    except:
        log('get info error')
    finally:
        cur.close()
        db.close()
        return res


def excute_sql(sql):
    db = None
    while not db:
        db = sqlite3.connect(sqlite_path)
        cur = db.cursor()
        try:
            cur.execute(sql)
            db.commit()
        except:
            log('excute info error')
        finally:
            cur.close()
            db.close()


def authentical(username, passwd):
    '''
    test user's validate
    :param username:
    :param passwd:
    :return:
    '''
    pwd = get_sql_info("select passwd from user where name = \'%s\' "%username)
    if pwd:
        return True if passwd == pwd[0][0] else False
    else:
        return False


@app.route('/index/')
def index():
    name = ''
    if 'name' in session:
        name = session['name']

    head = ['ID', 'Name', 'Start', 'End', 'User', 'Operate']
    res_list = get_sql_info("")
    res_dict = OrderedDict()
    count = 1
    for item in res_list:
        name, start, user = item
        res_dict[count] = {'Name':name, 'start':start, 'user':user}
        count += 1
    return render_template('index.html', res_list=res_list, res_dict=res_dict, head=head, name=name)


# @app.route('/login/', method=['POST', 'GET'])
# def login():
#     if request.method=='POST':
#         try:
#             user = request.form['name']
#             passwd = request.form['pwd']
#             if not authentical(user, passwd):
#                 error = 'Invalid username or password'
#                 return error
#         except:
#             if 'name' in session:
#                 user = session['name']
#         start = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
#         sql = 'Insert into user (name, start) values (\'%s\',\'%s\')'%(user, start)
#         excute_sql(sql)
#         return redirect(url_for('index'))
#
#
# @app.route('/cancel', methods=['GET'])
# def cancel():
#     name = request.args.get('name', '')
#     return redirect(url_for('index'))


@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        passwd = request.form['pwd']
        cpasswd = request.form['cpwd']
        if not passwd or not name:
            return 'Must has values'
        if passwd != cpasswd:
            return 'Password is different'
        return redirect(url_for('index'))
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')