from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register,name="register"),
    path('login', views.login,name="login"),
    path('post/', views.post,name="post"),
    path('details/',views.details,name="details")

]