import requests
from django.shortcuts import render
from django.contrib import messages
import time

def index(request):
    
    if request.method == 'POST':

        city = request.POST['city']
        
        weather_info = []

        r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=340ce8086f33079c4a4eb676ad2cfff3').json()
        print(r)

        if r['cod'] == 200:
            celsius_temp = round(((r['main']['temp'] - 32) * 5)/9, 1)
            sunrise = time.strftime("%H:%M:%S", time.gmtime(r['sys']['sunrise']))
            sunset = time.strftime("%H:%M:%S", time.gmtime(r['sys']['sunset']))


            weather = {
                'city' : city,
                'country': r['sys']['country'],
                'temperature' : celsius_temp,
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
                'wind' : r['wind']['speed'],
                'sunrise' : sunrise,
                'sunset' : sunset,
                'humidity' : r['main']['humidity']
            }
            weather_info.append(weather)

            context = {'weather_info' : weather_info, 
            }
            return render(request, 'weather.html', context)

        else: 
            messages.error(request, 'Not found! Please try another location or city.', extra_tags='alert')
            return render(request, 'weather.html')
            
    return render(request, 'weather.html')  