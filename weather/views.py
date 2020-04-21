from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
import json

def home(request):
    response = requests.get("http://api.ipstack.com/check?access_key=f7d722b02af8b6d1c7eacf4f4bbd86a2")
    geodata = response.json()
    return render(request, 'home.html', {
        'ip': geodata['ip'],
        'country': geodata["country_name"],
        'latitude': geodata["latitude"],
        'longitude': geodata["longitude"],
        'api_key': 'AIzaSyDCO9H3dVdsRJrSRrM77CYtKZTUl9ZqBzw'  # Don't do this! This is just an example. Secure your keys properly.
        })

def index(request):
    cities = City.objects.all() #return all the cities in the database

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate

    form = CityForm()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
        
        weather = {
            'city' : city,
            'country': city_weather['sys']['country'], 
            'temperature' : city_weather['main']['temp'],
            'pressure': city_weather['main']['pressure'], 
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list
    
    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather.html', context) 