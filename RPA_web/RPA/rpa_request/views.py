from django.shortcuts import render, redirect
from django.http import JsonResponse
import datetime
from .models import User


# Create your views here.


def index(request):
    return render(request, 'request/login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('password')
        print(username, passwd)
        data = {}
        num = User.objects.filter(username=username, passwd=passwd).count()
        print(num)
        if num > 0:
            info = User.objects.get(username=username)
            info.login_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            info.save()
            request.session['is_login'] = 1
            request.session['username'] = username
            data['is_select'] = 1
        else:
            data['is_select'] = 0
        return JsonResponse(data)
    return render(request, 'request/login.html')


def get_object(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return False


def register(request):
    if request.method == 'POST':
        office = request.POST.get('office')
        username = request.POST.get('username')
        passwd = request.POST.get('txtPwd')
        print(office, username, passwd)
        data = {
            'code': 200,
            'msg': '请求成功',
            'is_select': 1
        }

        if get_object(username):
            data['is_select'] = 0
        else:
            User.objects.create(username=username,
                                passwd=passwd,
                                login_time=datetime.datetime.now().strftime(
                                    '%Y-%m-%d %H:%M:%S'),
                                office=office)
            data['is_select'] = 1
        return JsonResponse(data)
    return render(request, 'request/register.html')
