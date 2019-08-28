from __future__ import unicode_literals
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict
from django.contrib import auth
import time
from . import models


sql_manage = models.sqlManage()


def authentical(username, passwd):
    '''
    test user's validate
    :param username:
    :param passwd:
    :return:
    '''
    pwd = sql_manage.get_sql_info("select passwd from user where name = \'%s\' "%username)
    if pwd:
        return True if passwd == pwd[0][0] else False
    else:
        return False


def index(request):
    name = ''
    if 'username' in request.session.keys():
        name = request.session['username']
    show_dict = OrderedDict()
    content = {'name':name, 'show_dict':show_dict}
    return render(request, 'index.html', content)


def login(request):
    if request.method == 'POST':
        try:
            user = request.POST.get('name', '')
            passwd = request.POST.get('pwd', '')
            file = request.POST.getlist('file', '')
            if not authentical(user, passwd):
                return HttpResponse('Invalid user or password')
            request.session['username'] = user
        except:
            if 'username' in request.session.keys():
                user = request.session['username']
                file = request.POST.getlist('file', '')
        return redirect('/index')


def logout(request):
    auth.logout(request)
    # request.session.clear()
    return redirect('/index')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        passwd = request.POST.get('pwd', '')
        confirm = request.POST.get('confirm', '')
        if not passwd or not name:
            return HttpResponse('Must has values')
        if passwd != confirm:
            return HttpResponse('Passwords are different')
        return redirect('/index')
    else:
        return render(request, 'register.html')
