from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.iqa_view, name='home'), 
    path('main/', views.iqa_view, name='main'),
]
