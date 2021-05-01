from django.shortcuts import render,HttpResponse,redirect
import datetime
from django.contrib.auth.decorators import login_required
from . models import MonthlyTotal,Expenses,List,WishList
from django.contrib.auth.models import User


# Create your views here.

@login_required
def index(request):
    if request.method == "GET":
        user1 = User.objects.get(username=request.user.username)
        if MonthlyTotal.objects.filter(user = user1).exists():
            user_info = MonthlyTotal.objects.get(user=user1)
            mincome = user_info.mincome 
            left = user_info.left          
            date1 = datetime.date.today()
            return render(request,"user/home.html",{
                'date' : date1,
                'mincome' : mincome,
                'left':left
            })
        else:
            date1 = datetime.date.today()
            return render(request,"user/home.html",{
                'date' : date1,
            })
                   
    if request.method == "POST":
        user1 = User.objects.get(username=request.user.username)
        if MonthlyTotal.objects.filter(user = user1).exists():
            user_info = MonthlyTotal.objects.get(user=user1)
            user_info.mincome = request.POST.get("mincome")
            user_info.left = request.POST.get("left")
            user_info.save()
            return redirect('index')
        else:
            mincome = request.POST.get("mincome")
            left = request.POST.get("left")
            date1 = datetime.date.today()
            m = MonthlyTotal(user=user1,mincome=mincome,left=left,date=date1)
            m.save()
            return redirect('index')
               
    else:
        return render(request,"user/home.html")
        
        
  
@login_required
def expenses(request):
    if request.method == "GET":
        user1 = User.objects.get(username=request.user.username)
        user_info = MonthlyTotal.objects.get(user=user1)
        if MonthlyTotal.objects.filter(user=user1).exists():
            li_info = List.objects.filter(user=user1)
            lis = li_info.all()
            expense_info = Expenses.objects.filter(user=user1)
            expenses = expense_info.all()
            mincome = user_info.mincome
            left = user_info.left
            
            lim = user_info.daily_limit
            
            time = datetime.datetime.now()
            return render(request,"user/expense.html",{
                'lis':lis,
                'expenses':expenses,
                'time':time,
                'mincome':mincome,
                'left':left,
                'lim':lim
            })
        
        return render(request,"user/expense.html")
    
    if request.method == "POST":
        user1 = User.objects.get(username=request.user.username)
        user_info = MonthlyTotal.objects.get(user=user1)
        category = request.POST.get("category")
        expense = request.POST.get("expense")
        cost = request.POST.get("cost")
        time = datetime.datetime.now()
        print(user_info.left)
        print(cost)
        lef = int(user_info.left)-int(cost)
        user_info.left = lef
        user_info.save()
        l = List(user=user1,name = category)
        l.save()
        u = Expenses(list_n=l,user=user1,expense=expense,cost=cost,created_at=time)
        u.save()
        return redirect('expenses')
        
    return render(request,"user/expense.html")

@login_required
def limit(request):
    if request.method == "GET":
        user1 = User.objects.get(username=request.user.username)
        if MonthlyTotal.objects.filter(user = user1).exists():
            user_info = MonthlyTotal.objects.get(user=user1)
            dailyLimit = user_info.daily_limit
            left = user_info.left
            d = int(left/30)
            dm = int(dailyLimit*30)
            sv = left - dm
            w = int(dailyLimit*7)
            a = int(d*7)
            wsv = a - w
            return render(request,"user/limit.html",{
                'dailyLimit': dailyLimit,
                'd':d,
                'sv':sv,
                'wsv':wsv
            })
        else:
            return render(request,"user/limit.html")
                   
    if request.method == "POST":
        user1 = User.objects.get(username=request.user.username)
        
        if MonthlyTotal.objects.filter(user = user1).exists():
            user_info = MonthlyTotal.objects.get(user=user1)
            user_info.daily_limit = request.POST.get("dailyLimit")
            user_info.save()
            return redirect('limit')
        
    return render(request,"user/limit.html")

@login_required
def goals(request):
    if request.method == "GET":
        user1 = User.objects.get(username=request.user.username)
        if WishList.objects.filter(user = user1):
            wish_info = WishList.objects.filter(user = user1)
            user_info = MonthlyTotal.objects.get(user=user1)
            dl = user_info.daily_limit
            mi = user_info.left
            me = dl*30
            sv = int(mi) - int(me)
            time = datetime.datetime.now()
            return render(request,"user/goals.html",{
            'wishes':wish_info,
            'time':time,
            'sv':sv
          })
        
    
    if request.method == "POST":
        user1 = User.objects.get(username = request.user.username)
        wish = request.POST.get("wish")
        exp = request.POST.get("exp")
        w = WishList(user=user1,wish=wish,exp=exp)
        w.save()
        return redirect("goals")
    return render(request,"user/goals.html")  

