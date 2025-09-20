from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import requests


def home(request):
    return render(request, "main/index.html")


def iqar(request):
    API_KEY = "de5c09f082acc1dd5b48d10c25095d22"

    capitais = [
        {"nome": "Rio Branco", "lat": -9.97, "lon": -67.81},
        {"nome": "Maceió", "lat": -9.67, "lon": -35.73},
        {"nome": "Macapá", "lat": 0.03, "lon": -51.07},
        {"nome": "Manaus", "lat": -3.1, "lon": -60.02},
        {"nome": "Salvador", "lat": -12.97, "lon": -38.5},
        {"nome": "Fortaleza", "lat": -3.73, "lon": -38.52},
        {"nome": "Brasília", "lat": -15.79, "lon": -47.88},
        {"nome": "Vitória", "lat": -20.32, "lon": -40.34},
        {"nome": "Goiânia", "lat": -16.68, "lon": -49.25},
        {"nome": "São Luís", "lat": -2.53, "lon": -44.3},
        {"nome": "Cuiabá", "lat": -15.6, "lon": -56.1},
        {"nome": "Campo Grande", "lat": -20.44, "lon": -54.62},
        {"nome": "Belo Horizonte", "lat": -19.92, "lon": -43.94},
        {"nome": "Belém", "lat": -1.46, "lon": -48.49},
        {"nome": "João Pessoa", "lat": -7.12, "lon": -34.86},
        {"nome": "Curitiba", "lat": -25.43, "lon": -49.27},
        {"nome": "Recife", "lat": -8.05, "lon": -34.9},
        {"nome": "Teresina", "lat": -5.09, "lon": -42.8},
        {"nome": "Rio de Janeiro", "lat": -22.91, "lon": -43.17},
        {"nome": "Natal", "lat": -5.79, "lon": -35.2},
        {"nome": "Porto Alegre", "lat": -30.03, "lon": -51.23},
        {"nome": "Porto Velho", "lat": -8.76, "lon": -63.9},
        {"nome": "Boa Vista", "lat": 2.82, "lon": -60.67},
        {"nome": "Florianópolis", "lat": -27.59, "lon": -48.55},
        {"nome": "São Paulo", "lat": -23.55, "lon": -46.63},
        {"nome": "Aracaju", "lat": -10.91, "lon": -37.07},
        {"nome": "Palmas", "lat": -10.25, "lon": -48.32},
    ]

    resultados = []

    for c in capitais:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={c['lat']}&lon={c['lon']}&appid={API_KEY}"
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()
            aqi = data["list"][0]["main"]["aqi"]
            components = data["list"][0]["components"]

        resultados.append({
            "cidade": c["nome"],
            "aqi_classificacao": aqi,   # de 1 a 5
            "pm2_5": components.get("pm2_5"),  # particulado fino
            "pm10": components.get("pm10"),    # particulado grosso
            "co": components.get("co"),        # monóxido de carbono
            "no2": components.get("no2"),      # dióxido de nitrogênio
            "o3": components.get("o3"),        # ozônio
            "so2": components.get("so2"),      # dióxido de enxofre
        })
    else:
        resultados.append({
            "cidade": c["nome"],
            "aqi_classificacao": None,
            "pm2_5": None,
            "pm10": None,
            "co": None,
            "no2": None,
            "o3": None,
            "so2": None,
        })

    return JsonResponse({"resultados": resultados})
