from django.urls import path

from . import views


urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('user/', views.UserView.as_view()),
    path('refresh/', views.RefreshTokenView.as_view()),
    path('user-activity/', views.UserActivityView.as_view()),
]