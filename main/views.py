from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import requests


def home(request):
    return render(request, "main/index.html")


def iqar(request):
    API_KEY = "de5c09f082acc1dd5b48d10c25095d22"

from django.http import JsonResponse
import requests

API_KEY = "de5c09f082acc1dd5b48d10c25095d22"

# Faixas de poluentes para o cálculo do AQI (EUA)
breakpoints = {
    "pm2_5": [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ],
    "pm10": [
        (0, 54, 0, 50),
        (55, 154, 51, 100),
        (155, 254, 101, 150),
        (255, 354, 151, 200),
        (355, 424, 201, 300),
        (425, 504, 301, 400),
        (505, 604, 401, 500),
    ],
    "co": [
        (0.0, 4.4, 0, 50),
        (4.5, 9.4, 51, 100),
        (9.5, 12.4, 101, 150),
        (12.5, 15.4, 151, 200),
        (15.5, 30.4, 201, 300),
        (30.5, 40.4, 301, 400),
        (40.5, 50.4, 401, 500),
    ],
    "so2": [
        (0, 35, 0, 50),
        (36, 75, 51, 100),
        (76, 185, 101, 150),
        (186, 304, 151, 200),
        (305, 604, 201, 300),
        (605, 804, 301, 400),
        (805, 1004, 401, 500),
    ],
    "no2": [
        (0, 53, 0, 50),
        (54, 100, 51, 100),
        (101, 360, 101, 150),
        (361, 649, 151, 200),
        (650, 1249, 201, 300),
        (1250, 1649, 301, 400),
        (1650, 2049, 401, 500),
    ],
    "o3": [  # 8h padrão
        (0, 54, 0, 50),
        (55, 70, 51, 100),
        (71, 85, 101, 150),
        (86, 105, 151, 200),
        (106, 200, 201, 300),
    ],
}

def calcular_aqi(polut, valor):
    """Calcula AQI de um poluente específico baseado em breakpoints"""
    if valor is None:
        return None
    for c_low, c_high, i_low, i_high in breakpoints[polut]:
        if c_low <= valor <= c_high:
            return round(((i_high - i_low) / (c_high - c_low)) * (valor - c_low) + i_low)
    return None

def iqar(request):
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
            components = data["list"][0]["components"]

            # calcula AQI para cada poluente
            aqi_por_pol = {
                "pm2_5": calcular_aqi("pm2_5", components.get("pm2_5")),
                "pm10": calcular_aqi("pm10", components.get("pm10")),
                "co": calcular_aqi("co", components.get("co")),
                "no2": calcular_aqi("no2", components.get("no2")),
                "o3": calcular_aqi("o3", components.get("o3")),
                "so2": calcular_aqi("so2", components.get("so2")),
            }

            # AQI final = o MAIOR dos poluentes
            aqi_final = max([v for v in aqi_por_pol.values() if v is not None], default=None)

            resultados.append({
                "cidade": c["nome"],
                "aqi_eua": aqi_final,
                "detalhes": aqi_por_pol,
                "pm2_5": components.get("pm2_5"),
                "pm10": components.get("pm10"),
                "co": components.get("co"),
                "no2": components.get("no2"),
                "o3": components.get("o3"),
                "so2": components.get("so2"),
            })
        else:
            resultados.append({
                "cidade": c["nome"],
                "aqi_eua": None,
                "detalhes": {},
            })

    return JsonResponse({"resultados": resultados})
