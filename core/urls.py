from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report_issue, name='report'),
    path('issues/', views.issue_list, name='issues'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
