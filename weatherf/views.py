import os
from django.shortcuts import render
import requests
from datetime import datetime

def index(request):
    try:
        city_weather_update = {}

        if request.method == 'POST':
            API_KEY = os.getenv('WEATHER_API_KEY')  # safer than hardcoding
            city_name = request.POST.get('city').strip()
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
            response = requests.get(url).json()

            print("API Response:", response)

            if response.get("cod") != 200:
                return render(request, 'weatherf/404.html', {"error": response.get("message")})

            current_time = datetime.now()
            formatted_time = current_time.strftime("%A, %B %d %Y, %H:%M:%S %p")

            city_weather_update = {
                'city': city_name,
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
                'temperature': f"Temperature: {response['main']['temp']} °C",
                'country_code': response['sys']['country'],
                'wind': f"Wind: {response['wind']['speed']} km/h",
                'humidity': f"Humidity: {response['main']['humidity']}%",
                'time': formatted_time
            }

        return render(request, 'weatherf/home.html', {'city_weather_update': city_weather_update})

    except Exception as e:
        return render(request, 'weatherf/404.html', {"error": str(e)})
