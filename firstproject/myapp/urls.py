from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('viewalldata/', views.viewalldata, name='viewalldata'),
    path('viewspecificdata/', views.viewspecificdata, name='viewspecificdata'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    path('deposit/', views.deposit, name='deposit'),
    path('balance/', views.balance, name='balance'),
]
