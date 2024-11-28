from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name="home"),
     path('my_page/', views.my_page, name="my_page"),
     path('edit_user_info/', views.edit_user_info, name="edit_user_info"),
     path('space_reg/', views.space_reg, name="space_reg"),
     path('booking_management/', views.booking_management, name='booking_management'),
     path('accept-booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
     path('reject-booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
     path('update-booking-status/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
     path('update_space/<int:space_id>/', views.update_space, name='update_space'),
     path('space/<int:space_id>/', views.space_detail, name='space_detail'),
     path('space/<int:space_id>/booking/', views.booking, name='booking'),
]

