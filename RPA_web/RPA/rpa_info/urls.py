

"""RPA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic.base import RedirectView
from django.urls import path
from . import views

urlpatterns = [
    path(r'favicon/.ico/', RedirectView.as_view(url=r"{% static 'img/bitbug_favicon.ico' %}")),
    path('', views.table, name='index'),
    path(r'table/', views.table, name='table'),
    path(r'ip_address/', views.ip_display, name='ip'),
    # path(r'chart/', views.chart, name='chart'),
    # path(r'chart1/', views.chart_1, name='chart1'),
    path(r'chart_pie/', views.chart_2, name='chart2'),
    # path(r'chart3/', views.chart_3, name='chart3'),
    path(r'chart_gather/', views.chart_4, name='chart4'),
    path(r'test/', views.test, name='test'),
    path(r'ip_edit/', views.ip_edit, name='ip_edit'),
    path(r'flow_edit/', views.flow_edit, name='flow_edit'),
    path(r'login/', views.login, name='login'),
    path(r'logout/', views.logout, name='logout'),
]
