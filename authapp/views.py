from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import auth,messages

# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request,"authapp/login.html")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                return redirect("index")
        else:
            return render(request,"authapp/login.html")
          
    
    return render(request,"authapp/login.html")

def register(request):
    if request.method == "GET":
        return render(request,"authapp/register.html")
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user1 = User.objects.create_user(password=password,username=username,first_name=firstname,last_name=lastname,email=email)
        user1.save()
        return redirect("login")
    return render(request,"authapp/register.html")

def logout(request):
    auth.logout(request)
    return redirect("login")