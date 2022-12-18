from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot-password/', views.forgotPassword,name='forgot-password'),
    path('', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reset-password-validate/<uidb64>/<token>/', views.resetPasswordValidate, name='reset-password-validate'),
    path('reset-password/', views.resetPassword, name='reset-password'),
]