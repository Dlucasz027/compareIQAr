from django.urls import path
from . import views

urlpatterns = [
    path('iqa/', views.iqa_view, name='iqa'),
]