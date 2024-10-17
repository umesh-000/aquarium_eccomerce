from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('mysite/customer_register/', views.customer_register, name='customer_register'),
    path('mysite/login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]