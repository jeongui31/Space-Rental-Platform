from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name="home"),
     path('my_page/', views.my_page, name="my_page"),
     path('space_reg/', views.space_reg, name="space_reg")
]