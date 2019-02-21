import time
'''

人
类名：Person
属性：姓名，身份证号，电话号，卡
行为：

卡：
类名：Card
属性：卡号，密码，余额
行为：

银行
类名：Bank
属性：用户列表，提款机

提款机
类名：ATM
属性：
行为：开户，查询，取款，存储，转账，改密，锁定，解锁，补卡，销户，退出


管理员
类名：Admin
属性：
行为：管理员界面， 管理员登录， 系统功能界面

'''

class Admin(object):
    def __init__(self):
        self.admin = '1'
        self.passwd = '1'

    def printAdminView(self):
        print('*****************************')
        print('*                           *')
        print('*                           *')
        print('*     欢迎登录银行          *')
        print('*                           *')
        print('*                           *')
        print('*****************************')

    def printSysFunctionView(self):
        print('*********************************************')
        print('*         开户(1)        查询（2）          *')
        print('*         取款(3)        存款（4）          *')
        print('*         转账(5)        改密（6）          *')
        print('*         锁定(7)        解锁（8）          *')
        print('*         补卡(9)        销户（0）          *')
        print('*                退出(quit)                 *')
        print('*                                           *')
        print('*                                           *')
        print('*********************************************')
    def adminOption(self):
        inputAdmin = input("输入管理员账号")
        if self.admin != inputAdmin:
            print('账号有误')
            return -1
        inputPasswd = input("输入密码")
        if self.passwd != inputPasswd:
            print('密码有误')
            return -1
        print('操作成功！请稍后.....')
        time.sleep(2)
        return 0

class Card(object):
    def __init__(self, cardId, cardPasswd, cardMoney):
        self.cardId = cardId
        self.cardPasswd = cardPasswd
        self.cardMoney = cardMoney
class User(object):
    def __init__(self, name, idCard, phone, card):
        self.name = name
        self.idCard = idCard
        self.phone = phone
        self.card = card
# from user import User
# from card import Card
class ATM(object):
    def __init__(self):
        self.allUser = {}
    def creatUser(self):
        #向用户字典中添加一对键值对（卡号-用户）
        name = input('请输入您的姓名：')
        idCard = input('请输入您的身份证号：')
        phone = input('请输入您的手机号：')
        prestoreMoney = float(input('请输入预存款金额：'))
        if prestoreMoney < 0:
            print('金额有误，开户失败')
            return -1
        onePasswd = int(input('请设置密码：'))
    def searchUserInfo(self):
        pass
    def getMoney(self):
        pass
    def saveMoney(self):
        pass
    def transferMoney(self):
        pass
    def changePasswd(self):
        pass
    def lockUser(self):
        pass
    def unlockUser(self):
        pass
    def newCard(self):
        pass
    def killUser(self):
        pass

def main():
    #界面对象
    view = Admin()
    view.printAdminView()
    if view.adminOption():
        return -1


    atm = ATM()

    while True:
        view.printSysFunctionView()
        #等待用户操作
        option = input("请输入操作")
        if option == "1":
            #开户
            print('开户')
            atm.creatUser()
        if option == "2":
            #查询
            print('查询')
        if option == "3":
            #取款
            print('取款')
        if option == "4":
            #存款
            print('存款')
        if option == "5":
            #转账
            print('转账')
        if option == "6":
            #改密
            print('改密')
        if option == "7":
            #锁定
            print('锁定')
        if option == "8":
            #解锁
            print('解锁')
        if option == "0":
            #销户
            print('销户')
        if option == "quit":
            #退出
            if not view.adminOption():
                print('退出')
                return -1
        time.sleep(2)




if __name__ == '__main__':
    main()


