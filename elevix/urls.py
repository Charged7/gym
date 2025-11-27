from django.urls import path
from . import views

app_name = 'elevix'

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    path('trainers/', views.trainers_list, name='trainers_list'),
    path('trainers/<int:pk>/', views.trainer_detail, name='trainer_detail'),
]