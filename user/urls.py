from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('expenses/',views.expenses,name="expenses"),
   path('limit/',views.limit,name="limit"),
   path('goals/',views.goals,name="goals"),
]