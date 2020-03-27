from django.shortcuts import render, redirect
import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'MyDjango.settings')
django.setup()
from .models import Rpa
# Create your views here.


def index(request):
    flow = Rpa.objects.all()
    print(flow)
    return render(request, 'index.html')



if __name__ == '__main__':
    index(request='POST')

