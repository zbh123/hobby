'''

人
类名：Person
属性：gun
行为：fire

枪
类名：Gun
属性：bulletBox
行为：shoot

弹夹
'''

class BulletBox(object):
    def __init__(self,count):
        self.bulletCount = count

class Gun(object):
    def __init__(self, bulletBox):
        self.bulletBox = bulletBox
    def shoot(self):
        if self.bulletBox.bulletCount == 0:
            print('out')
        else:
            self.bulletBox.bulletCount -= 1
            print('剩余子弹：%d发'%self.bulletBox.bulletCount)

class Person(object):
    def __init__(self, gun):
        self.gun = gun
    def fire(self):
        self.gun.shoot()
    def fillBullet(self, count):
        self.gun.bulletBox.bulletCount = count


bulletBox = BulletBox(5)

gun = Gun(bulletBox)

per = Person(gun)

per.fire()
per.fire()
per.fire()
per.fire()
per.fire()
per.fire()
per.fillBullet(2)
per.fire()
per.fire()
per.fire()











