from django.shortcuts import render,HttpResponse,redirect
import datetime
from django.contrib.auth.decorators import login_required
from . models import MonthlyTotal,Expenses,List,WishList
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.db.models import Sum
    
import csv
from django.utils.encoding import smart_str


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
            pdsv = d - dailyLimit
           
            
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
        i = 0
        a = 0
        ws = ''
        user1 = User.objects.get(username=request.user.username)
        if WishList.objects.filter(user = user1):
            wish_info = WishList.objects.filter(user = user1)
            user_info = MonthlyTotal.objects.get(user=user1)
            dl = user_info.daily_limit
            mi = user_info.left
            d = int(mi/30)
            pdsv = int(d - dl)
            for wish in wish_info:
                for i in range(100):
                    if pdsv*i >= wish.exp:
                        a = i
                        ws = wish.wish
                        break
            
            me = dl*30
            sv = int(mi) - int(me)
            time = datetime.datetime.now()
            return render(request,"user/goals.html",{
            'wishes':wish_info,
            'time':time,
            'sv':sv,
            'pdsv':pdsv,
            'a':a,
            'ws':ws
          })
        
    
    if request.method == "POST":
    
        user1 = User.objects.get(username = request.user.username)
        if WishList.objects.filter(user = user1):  
            wish_info = WishList.objects.filter(user = user1)
            user_info = MonthlyTotal.objects.get(user=user1)
            dl = user_info.daily_limit
            mi = user_info.left
            d = int(mi/30)
            pdsv = int(d - dl)
                    
        wish = request.POST.get("wish")
        exp = request.POST.get("exp")
        w = WishList(user=user1,wish=wish,exp=exp)
        w.save()
        return redirect("goals")
    return render(request,"user/goals.html")  


class ChartView(TemplateView):
    template_name = 'chart/chart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user2 = User.objects.get(username=self.request.user.username)
        context["qs"] = Expenses.objects.filter(user=user2) 
        return context
    
    
class PieView(TemplateView):
    template_name = 'chart/pie.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user2 = User.objects.get(username=self.request.user.username)
        context["qs"] = Expenses.objects.filter(user=user2) 
        return context
    
    
class DoView(TemplateView):
    template_name = 'chart/doughnut.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user2 = User.objects.get(username=self.request.user.username)
        context["qs"] = Expenses.objects.filter(user=user2) 
        return context
    

def download_csv_data(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="User.csv"'
    
    writer = csv.writer(response,csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
  
    writer.writerow([
        smart_str(u"Date and Time"),
        smart_str(u"Expenses"),
        smart_str(u"Cost"),
        
        ])
    user1 = User.objects.get(username=request.user.username)
    exps = Expenses.objects.filter(user=user1)
    for exp in exps:
       
        writer.writerow([
            smart_str(exp.created_at),
            smart_str(exp.expense),
            smart_str(exp.cost),
            
            ])
    writer.writerow(['','','',''])
    writer.writerow(['TOTAL','',str(exps.aggregate(Sum('cost'))['cost__sum'])])
    return response



