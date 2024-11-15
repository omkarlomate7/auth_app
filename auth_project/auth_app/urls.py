from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('landing/', views.landing_view, name='landing_page'), 
    path('logout/', views.logout_view, name='logout'), 
]