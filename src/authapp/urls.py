from django.urls import path
from . import views

app_name = 'authapp'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('profile/<int:pk>', views.UserDetails.as_view(), name='profile'),
]