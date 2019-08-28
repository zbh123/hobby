from django.db import models

# Create your models here.
from django.db import connection


class sqlManage(models.Manager):

    def get_sql_info(self,sql):
        cur = connection.cursor()
        try:
            cur.execute(sql)
            res = cur.fetchall()
        except:
            res = []
        finally:
            cur.close()
        return res

    def execute(self, sql):
        cur = connection.cursor()
        try:
            cur.execute(sql)
        finally:
            cur.close()
