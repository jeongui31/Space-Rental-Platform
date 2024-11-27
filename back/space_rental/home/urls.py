from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name="home"),
     path('my_page/', views.my_page, name="my_page"),
     path('edit_user_info/', views.edit_user_info, name="edit_user_info"),
     path('space_reg/', views.space_reg, name="space_reg"),
     path('booking_management/', views.booking_management, name='booking_management'),
     path('update_space/<int:space_id>/', views.update_space, name='update_space'),
     path('space/<int:space_id>/', views.space_detail, name='space_detail'),
]

