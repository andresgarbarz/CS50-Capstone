# Weather50

## Distinctiveness and Complexity

The project satisfies the distinctiveness and complexity requirements for capstone because:

1. The main idea of the website is completely different from the previous projects.
    - Project 0 - Search: It does not consist of just html/css and it has nothing to do with a search engine.
    - Project 1 - Wiki: It is not an articles website and users cannot create nor edit any information available.
    - Project 2 - Commerce: It is not an e-commerce website nor anything related with pucharsing stuff on the web.
    - Project 3 - Mail: It is not an email client nor a communication platform.
    - Project 4 - Network: It is not a social network and users cannot interact with each other.

2. The project complexity relies mostly on the APIs, services and libraries used. It is more complex than the previous ones because of the way it implements all of this, which cannot be seen in any of the other projects.

    - The combination of the _wikipedia_, _requests_ and _json_ python libraries to extract the cities information and picture from wikipedia.
    - The combination of the openweathermap.org "Current Weather" and "Air Pollution" API services with _requests_, _json_, _country\_converter_ and _datetime_ libraries to get the real-time weather information.

    For my final project, I decided to work with an API service as it was not something used in any of the other projects and it was a good way to familiarize myself with the python requests library. My first idea was to make a weather forecast app, which allowed users to see the current weather in any city of the world. However, I quickly realized that was a fairly simple idea, so I decided to make it better, adding some interesting stuff on the road to enrich the project. Thus, I added air quality index, cities information, map rendering with their location and a favorite cities section.

## Content of each file

The django project is called "finalproject" and it has a single app in it called "weather".

Django default files I worked most with:

- _views.py_: Main python logic file. Contains the functions responsible for receiveing multiple requests and sending different responses according to the situation. It also has the logic for the interaction with the APIs and the data extraction.

- _models.py_: Django models file. Contains the User, City and Preferences models stored as tables in the sqlite3 database, with their respective fields and relationships. Disclaimer: The image and information texts about the cities is not stored because it might change since it comes from a wikipedia article.

- _weather/urls.py_: Weather app URLs file. Contains the logic responsible for connecting the URLs with their respective request-response functions.

- _admin.py_: Django admin file. Contains the register of the Django Models into the admin page, in order to easily manipulate them.

There are a few files apart from django default files:

- _layout.html_: HTML layout file from which all pages are built. Contains the head of each html page and the navbar.

- _login.html_: Login page. Contains the form to log in.
- _register.html_: Register page. Contains the form to sign up.

- _index.html_: Landing page.
- _index.js_: Javascript logic for the landing page. Contains the function for the loading spinner and text.

- _city.html_: City page. Displays the information and weather of the city queried.
- _main.js_: Javascript logic for the "City" page. Contains the functions responsible of loading the map, adding/removing the city from the users favorites and the expand/shrink information button's logic.

- _mycities.html_: My Cities page. Displays a map full of markers for the user's favorite cities, as well as cards on the right of it.
- _mycities.js_: Javascript logic for the "My Cities" page. Contains the functions responsible of loading the map, filling it with random-colored markers for the favorite cities and the info button's logic.

- _styles.css_: Styling of all the frontend.
- _fav.png_: Image used for the add to favorite button animation.
- _weatherbg.png_: Image shown in the background of all pages.
- _weatherlogo.png_: Icon displayed at the left in the navbar.

## How to run the application

After all python libraries written in "requirements.txt" are succesfully installed, to run the application you just need to write "python manage.py runserver" in a terminal, in which the current directory is the folder "finalproject". Then, you should open the browser of your preference at the port (localhost:portnumber) shown in the terminal (usually 8000, so localhost:8000).

## What you can do

Weather50 let's you...

- Register/Log In/Log Out.
- Search for a city. You can pass the country as an additional parameter using ",".
    - See the weather and air pollution data in real time.
    - See an image and the information about the city, which you can expand/shrink.
    - Navigate through an interactive map with a red pointer at the city.
    - Add the city to the user favorites (if logged in).
- Choose your measurement unit at the preferences section (if logged in).
- See an interactive map full of colorful pointers at the user's favorite cities (if logged in).