from django.shortcuts import render
from .models import Wheel
# Create your views here.

def home(request):
    # wheelsList = Wheel.objects.all()
    list_img = ['/static/home/img/2.jpg', '/static/home/img/10.jpg', '/static/home/img/11.jpg', '/static/home/img/12.jpg']
    list_nav = {'每日签到': '/static/home/img/2.jpg', '每日必修': '/static/home/img/10.jpg', '现正直播': '/static/home/img/11.jpg',
                '极力推荐': '/static/home/img/12.jpg'}
    list_menu = ['/static/home/img/10.jpg', '/static/home/img/11.jpg', '/static/home/img/12.jpg', '/static/home/img/2.jpg']

    return render(request, 'axf/home.html', {'title': '主页', 'list_img': list_img, 'list_nav': list_nav,
                                            "list_menu": list_menu, "shop1_img": '/static/home/img/2.jpg',
                                             "shop1_name": '便利商店'})

def market(request):
    return render(request, 'axf/market.html', {'title': '闪送超市'})

def cart(request):
    return render(request, 'axf/cart.html', {'title': '购物车'})

def mine(request):
    return render(request, 'axf/mine.html', {'title': '我的'})






