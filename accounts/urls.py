from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit', views.profile, name="profile_edit"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
]
