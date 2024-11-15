from django.contrib import admin
from django.urls import path, include
from auth_app import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('', views.home_view, name='home'),  
]