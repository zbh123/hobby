from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/', views.home, name="home"),
    url(r'^market/', views.market, name="market"),
    url(r'^cart/', views.cart, name="cart"),
    url(r'^mine/', views.mine, name="mine"),

]



