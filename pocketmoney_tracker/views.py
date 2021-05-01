from django.shortcuts import render,HttpResponse,redirect
import datetime

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User


def login1(request):
    return render(request,"authapp/register.html")