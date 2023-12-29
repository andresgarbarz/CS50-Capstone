from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search, name="search"),
    path("preferences", views.preferences, name="preferences"),
    path("newunit", views.newunit, name="newunit"),
    path("fav", views.fav, name="fav"),
    path("mycities", views.mycities, name="mycities")
]