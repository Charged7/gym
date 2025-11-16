from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users, name='users'),
    path('trener-shablon/', views.trener_shablon, name='trener_shablon'),
    path('trener-cabinet/', views.trener_cabinet, name='trener_cabinet'),
    path('trener-edit/', views.trener_edit, name='trener_edit'),
    path('login/', views.login, name='login'),
    path("register/", views.register_gym_user, name="register"),
    path("profile/", views.user_profile, name="user_profile"),
    path('reset_password_request/', views.reset_password_request, name='reset_password_request'),
    path('logout/', views.logout_view, name='logout'),
]