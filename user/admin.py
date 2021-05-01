from django.contrib import admin
from . models import MonthlyTotal,Expenses,List,WishList

# Register your models here.

admin.site.register(MonthlyTotal)
admin.site.register(Expenses)
admin.site.register(List)
admin.site.register(WishList)




