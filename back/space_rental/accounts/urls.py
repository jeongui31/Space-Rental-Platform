from django.urls import path
from django.contrib.auth.views import LogoutView


from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]