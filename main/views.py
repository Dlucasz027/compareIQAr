import requests
from django.shortcuts import render
from django.conf import settings

url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={cidade['lat']}&lon={cidade['lon']}&appid={settings.API_KEY}"

capitais = [
    {"nome": "São Paulo", "lat": -23.5505, "lon": -46.6333},
    {"nome": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
    {"nome": "Belo Horizonte", "lat": -19.9167, "lon": -43.9345},
    {"nome": "Brasília", "lat": -15.7939, "lon": -47.8828},
    {"nome": "Salvador", "lat": -12.9777, "lon": -38.5016},
    {"nome": "Fortaleza", "lat": -3.7172, "lon": -38.5433},
    {"nome": "Curitiba", "lat": -25.4284, "lon": -49.2733},
    {"nome": "Recife", "lat": -8.0476, "lon": -34.8770},
    {"nome": "Porto Alegre", "lat": -30.0346, "lon": -51.2177},
    {"nome": "Manaus", "lat": -3.1019, "lon": -60.0250},
    {"nome": "Belém", "lat": -1.4550, "lon": -48.5020},
    {"nome": "Goiânia", "lat": -16.6869, "lon": -49.2648},
    {"nome": "São Luís", "lat": -2.5307, "lon": -44.3068},
    {"nome": "Maceió", "lat": -9.6659, "lon": -35.7350},
    {"nome": "Natal", "lat": -5.7950, "lon": -35.2094},
    {"nome": "João Pessoa", "lat": -7.1150, "lon": -34.8631},
    {"nome": "Teresina", "lat": -5.0892, "lon": -42.8016},
    {"nome": "Campo Grande", "lat": -20.4428, "lon": -54.6462},
    {"nome": "Cuiabá", "lat": -15.6010, "lon": -56.0979},
    {"nome": "Florianópolis", "lat": -27.5945, "lon": -48.5477},
    {"nome": "Vitória", "lat": -20.3155, "lon": -40.3128},
    {"nome": "Aracaju", "lat": -10.9472, "lon": -37.0731},
    {"nome": "Macapá", "lat": 0.0389, "lon": -51.0664},
    {"nome": "Palmas", "lat": -10.2450, "lon": -48.3558},
    {"nome": "Boa Vista", "lat": 2.8196, "lon": -60.6738},
    {"nome": "Porto Velho", "lat": -8.7608, "lon": -63.8999},
    {"nome": "Rio Branco", "lat": -9.9747, "lon": -67.8243},
]

def iqa_view(request):
    capitais_iqa = []

    for cidade in capitais:
        try:
            url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={cidade['lat']}&lon={cidade['lon']}&appid={API_KEY}"
            resp = requests.get(url, timeout=5).json()
            aqi = resp["list"][0]["main"]["aqi"]
            capitais_iqa.append({"nome": cidade["nome"], "aqi": aqi})
        except:
            pass

    capitais_iqa_sorted = sorted(capitais_iqa, key=lambda x: x["aqi"])
    melhores = capitais_iqa_sorted[:10]
    piores = capitais_iqa_sorted[-10:]

    # retorna para o template HTML
    return render(request, "iqa.html", {"melhores": melhores, "piores": piores})