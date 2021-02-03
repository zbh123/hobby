

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
    path(r'index', views.index, name='index'),
    path(r'flowchart_info/<int:workflow_id>/states', views.WorkflowStateView.as_view(), name='flowchart_info'),
    path(r'flowinfo', views.workflow_infomation, name='workflow_infomation'),

]
