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
from django.contrib import admin
from django.conf.urls import include
from django.views.generic.base import RedirectView
from django.urls import path
import rpa_info, rpa_request, rpa_command

urlpatterns = [
    path('admin/', admin.site.urls),
    # path(r'', include(('rpa_info.urls', "info"), namespace="info")),
    path(r'info/', include(('rpa_info.urls', "info"), namespace="info")),
    path(r'request/', include(('rpa_request.urls', "request"), namespace="request")),
    path(r'command/', include(('rpa_command.urls', "command"), namespace="command")),
]
