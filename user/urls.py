from django.contrib import admin
from django.urls import path
from . import views
from . views import ChartView,PieView,DoView

urlpatterns = [
    path('', views.index,name="index"),
    path('expenses/',views.expenses,name="expenses"),
   path('limit/',views.limit,name="limit"),
   path('goals/',views.goals,name="goals"),
   path('chart/',ChartView.as_view(),name = "chart"),
   path('pie/',PieView.as_view(),name = "pie"),
   path('doughnut/',DoView.as_view(),name = "doughnut"),
   path('downloadcsv/',views.download_csv_data,name = "downloadcsv"),
    
]