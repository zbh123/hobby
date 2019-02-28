import time
import random
import pickle
import os
'''

人
类名：Person
属性：姓名，身份证号，电话号，卡
行为：

卡：
类名：Card
属性：卡号，密码，余额
行为：

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
        self.cardLock = False
class User(object):
    def __init__(self, name, idCard, phone, card):
        self.name = name
        self.idCard = idCard
        self.phone = phone
        self.card = card


class ATM(object):
    def __init__(self, allUser):
        self.allUser = allUser #卡号-用户
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
        #验证密码
        if not self.checkPasswd(onePasswd):
            print('密码错误，开户失败')
            return -1

        cardStr = self.randomCardId()
        card = Card(cardStr, onePasswd, prestoreMoney)
        user = User(name, idCard, phone, card)
        self.allUser[cardStr] = user
        print('开户成功！！！')
        print('您的卡号是：%s'%cardStr)

    #查询
    def searchUserInfo(self):
        cardNum = input('请输入卡号：')
        user = self.allUser.get(cardNum)
        if not self.checkInfo(user):
            return -1
        print('账号： %s     余额：%d'%(user.card.cardId, user.card.cardMoney))
    #取款
    def getMoney(self):
        cardNum = input('请输入卡号：')
        user = self.allUser.get(cardNum)
        if not self.checkInfo(user):
            return -1
        print('账号： %s     余额：%d' % (user.card.cardId, user.card.cardMoney))
        tmpMoney = float(input('请输入取款金额：'))
        if tmpMoney > user.card.cardMoney:
            print('余额不足，取款失败')
            return -1
        user.card.cardMoney -= tmpMoney
        print('取款成功，剩余金额 %d'%user.card.cardMoney)
    #存款
    def saveMoney(self):
        cardNum = input('请输入卡号：')
        user = self.allUser.get(cardNum)
        if not self.checkInfo(user):
            return -1
        print('账号： %s     余额：%d' % (user.card.cardId, user.card.cardMoney))
        tmpMoney = float(input('请输入存款金额：'))
        if tmpMoney < 0:
            print('数值有误，存款失败')
            return -1
        user.card.cardMoney += tmpMoney
        print('存款成功，剩余金额 %d' % user.card.cardMoney)
    #转账
    def transferMoney(self):
        pass
    #改密码
    def changePasswd(self):
        cardNum = input('请输入卡号：')
        user = self.allUser.get(cardNum)
        if not self.checkInfo(user):
            return -1
        newPasswd = input('请输入新密码：')
        newPasswdConfirm = input('请确认密码：')
        if newPasswd != newPasswdConfirm:
            print('两次密码输入不同，请重新操作')
            changePasswd()
        else:
            user.card.cardPasswd = newPasswd
            print('改密成功，新密码是' + user.card.cardPasswd)
    #锁定账户
    def lockUser(self):
        cardNum = input('请输入卡号：')
        user = self.allUser.get(cardNum)
        if not self.checkInfo(user):
            return -1
        tempIdCard = input("请输入身份证号：")
        if tempIdCard != user.idCard:
            print('身份输入有误，锁定失败')
            return -1
        user.card.cardLock = True
        print('锁定成功')
    #解锁账户
    def unlockUser(self):
        cardNum = input('请输入卡号：')
        user = self.allUser.get(cardNum)
        if not user:
            print('卡号不存在，解锁失败')
            return -1
        if not user.card.cardLock:
            print('改卡未锁定，无需解锁')
            return -1
        if not self.checkPasswd(user.card.cardPasswd):
            print('密码错误，解锁失败')
            return -1
        tempIdCard = input("请输入身份证号：")
        if tempIdCard != user.idCard:
            print('身份输入有误，解锁失败')
            return -1
        user.card.cardLock = False
        print('解锁成功')
    #办理新卡
    def newCard(self):
        pass
    #销户
    def killUser(self):
        cardNum = input('请输入卡号：')
        user = self.allUser.get(cardNum)
        if not self.checkInfo(user):
            return -1
        confirminfo = input('请确认是否销户，确认销户请输入Y，取消销户请输入N：')
        if confirminfo == 'N' or confirminfo =='Not':
            print('取消操作成功')
            return -1
        deleteInfo = self.allUser.pop(cardNum)
        print('销户成功')
        print(deleteInfo)
    #验证密码
    def checkPasswd(self, realPasswd):
        for i in range(3):
            tmpPasswd = int(input("请输入密码："))
            if tmpPasswd == realPasswd:
                print('密码正确')
                return 1
        return False
    def randomCardId(self):
        str = ""
        for i in range(6):
            ty = random.randrange(3)
            ty = 2
            if ty == 0 :
                #随机生成大写字母
                ch = chr(random.randrange(ord('A'),ord('Z')+1))
                str += ch
            elif ty == 1:
                #随机生成小写字母
                ch = chr(random.randrange(ord('a'),ord('z')+1))
                str += ch
            else:
                #随机生成数字
                ch = chr(random.randrange(ord('0'),ord('9')+1))
                str += ch
        if not self.allUser.get(str):
            return str
    def checkInfo(self, user):
        if not user:
            print('卡号不存在')
            return False
        # 验证锁定
        if user.card.cardLock:
            print('改卡被锁定，请解锁')
            return False
        # 验证密码
        if not self.checkPasswd(user.card.cardPasswd):
            print('密码错误')
            return False
        return True


def main():
    #界面对象
    view = Admin()
    view.printAdminView()
    if view.adminOption():
        return -1
    filepath = os.path.join(os.getcwd(), "alluser.txt")
    f = open(filepath, 'rb')
    allUser = pickle.load(f)

    atm = ATM(allUser)

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
            atm.searchUserInfo()
        if option == "3":
            #取款
            print('取款')
            atm.getMoney()
        if option == "4":
            #存款
            print('存款')
            atm.saveMoney()
        if option == "5":
            #转账
            print('转账')
        if option == "6":
            #改密
            print('改密')
            atm.changePasswd()
        if option == "7":
            #锁定
            atm.lockUser()
            print('锁定')
        if option == "8":
            #解锁
            atm.unlockUser()
            print('解锁')
        if option == "0":
            #销户
            atm.killUser()
            print('销户')
        if option == "quit":
            #退出
            if not view.adminOption():
                print('退出')
                filepath = os.path.join(os.getcwd(),"alluser.txt")
                print(filepath)
                f = open(filepath,'wb')
                pickle.dump(atm.allUser, f)
                f.close()

                return -1

        # 保存数据

        time.sleep(2)




if __name__ == '__main__':
    main()


