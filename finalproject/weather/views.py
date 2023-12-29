from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm

from .models import User
from .models import Preferences
from .models import City

import requests, json, wikipedia, re
import country_converter as coco
from datetime import datetime

def index(request):
    return render(request, "weather/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "weather/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "weather/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "weather/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "weather/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "weather/register.html")

api_key = "b0307c6728403fa89657bd7a02bb2d70"
wurl = "https://api.openweathermap.org/data/2.5/weather?q="
aurl = "http://api.openweathermap.org/data/2.5/air_pollution?"
title = None

def search(request):
    city = request.GET.get("q")
    if not city:
        return render(request, "weather/index.html", {
            "message": "City not found"
        })
    city = convertcity(city)
    
    # Get user unit from preferences model or use standard
    try:
        pref = Preferences.objects.get(user=request.user)
        unit = re.sub('[^0-9a-zA-Z]+', '', pref.unit.lower())
        unit = unit[:int(len(unit)/2)]
    except:
        unit = 'standard'

    # Convert it to temp and speed units
    if unit == 'standard':
        tempunit = 'K'
        speedunit = 'm/s'
    elif unit == 'metric':
        tempunit = '°C'
        speedunit = 'm/s'
    else:
        tempunit = '°F'
        speedunit = 'mph'

    # Request the weather
    req = wurl + city + "&appid=" + api_key + "&units=" + unit
    res = requests.get(req)
    data = res.json()
    if data["cod"] == "404":
        return render(request, "weather/index.html", {
            "message": "City not found"
        })
    else:
        # Check if city is already in the database
        try:
            citydb = City.objects.get(id=data["id"])
            if request.user in citydb.favs.all():
                fav = "is-active"
            else:
                fav = ""
        except City.DoesNotExist:
            # Add city to the database
            fav = ""
            citydb = City(id = data["id"], lon = data["coord"]["lon"], lat = data["coord"]["lat"], name = data["name"], country = data["sys"]["country"])
            citydb.save()
        
        # Make air pollution request
        req = aurl + "lon=" + str(data["coord"]["lon"]) + "&lat=" + str(data["coord"]["lat"]) + "&appid=" + api_key
        res = requests.get(req)
        aqi = res.json()["list"][0]["main"]["aqi"]

        # Search wikipedia image for the city
        country = data["sys"]["country"]
        image = getImage(data["name"] + " " + country)
        if not image:
            # Try again with the country converted to ISO2
            image = getImage(data["name"] + " " + coco.convert(names=country, to='ISO2'))
        # Make request to get wikipedia info for the city
        try:
            req = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/" + title)
            info = req.json()["extract"]
            infolist = info.split('. ')
        except:
            summary = None
            info = None
        else:
            # Convert response to summary and info variables, varying amount of sentences
            try:
                summary = summarize(infolist, 1)
                info = summarize(infolist, 3)
            except IndexError:
                summary = infolist[0] + '.'        
        # In case info could not be returned
        if "may refer to" in summary:
            summary = None

        return render(request, "weather/city.html", {
            "data": data,
            "weather": data["weather"][0],
            "image": image,
            "summary": summary,
            "info": info,
            "sunset": {"UTC": (datetime.utcfromtimestamp(int(data["sys"]["sunset"])).strftime('%Y-%m-%d %H:%M:%S'))[11:], "local": (datetime.utcfromtimestamp(int(data["sys"]["sunset"])+int(data["timezone"])).strftime('%Y-%m-%d %H:%M:%S'))[11:]},
            "sunrise": {"UTC": (datetime.utcfromtimestamp(int(data["sys"]["sunrise"])).strftime('%Y-%m-%d %H:%M:%S'))[11:], "local": (datetime.utcfromtimestamp(int(data["sys"]["sunrise"])+int(data["timezone"])).strftime('%Y-%m-%d %H:%M:%S'))[11:]},
            "aqi": aqi,
            "tempunit": tempunit,
            "speedunit": speedunit,
            "fav": fav
        })

@login_required
def preferences(request):
    pref = Preferences.objects.get(user=request.user)
    unit = re.sub('[^0-9a-zA-Z]+', '', pref.unit.lower())
    unit = unit[:int(len(unit)/2)]
    return render(request, "weather/preferences.html", {
            "checked": {unit: "checked"}
        })

@login_required
def newunit(request):
    data = json.loads(request.body)
    newunit = data["unit"].capitalize()
    pref = Preferences.objects.get(user=request.user)
    pref.unit = (newunit, newunit)
    pref.save()
    return HttpResponse(status=204)

@login_required
def fav(request):
    data = json.loads(request.body)
    city = City.objects.get(id=data["id"])
    if request.user in city.favs.all():
        city.favs.remove(request.user)
    else:
        city.favs.add(request.user)
    city.save()
    return HttpResponse(status=204)

@login_required
def mycities(request):
    cities = list(request.user.cities.all().values())
    return render(request, "weather/mycities.html", {
        "cities": cities
    })

wreq = 'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='
def getImage(search):
    global title
    try:
        result = wikipedia.search(search, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        res  = requests.get(wreq + title)
        data = json.loads(res.text)
        img = list(data['query']['pages'].values())[0]['original']['source']
        return img
    except:
        return None

def summarize(infolist, num):
    summary = ""
    for i in range(num):
        if infolist[1][0].isupper():
            summary = summary + infolist[0] + '. '
        else:
            summary = summary + infolist[0] + '. ' + infolist[1].split('. ')[0] + '. '
        infolist.pop()
    return summary

def convertcity(city):
    if "," in city:
        city = city.split(",")
        country = coco.convert(names=city[1], to='ISO2')
        city = city[0] + ", " + country
        city.replace(",", "%2C")
    city.replace(" ", "+")
    return city