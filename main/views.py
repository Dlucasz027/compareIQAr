from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import requests

def home(request):
    return render (request, "main/index.html")

def iqar(request):
    API_KEY = "de5c09f082acc1dd5b48d10c25095d22"

    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={-23.55}&lon={-46.63}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Erro interno"}, status=500)