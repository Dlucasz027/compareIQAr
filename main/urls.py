from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home_principal"),
    path("iqar/", views.iqar, name="funcao_iqar"),
]
