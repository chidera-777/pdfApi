from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path('register/', views.register_apiView, name="auth_register"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('logout/', knox_views.LogoutView.as_view(), name="logout"),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name="logoutall"),
 ]