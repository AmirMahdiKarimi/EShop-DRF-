from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('logout/', views.LogoutView.as_view(), name="knox-logout"),
    path('user/', views.UserAPIView.as_view()),
    path('change_password/', views.ChangePassAPIView.as_view()),
    path('set_profile/', views.SetProfileAPIView.as_view()),
]
