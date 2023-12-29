from django.contrib import admin

from .models import User
from .models import City
from .models import Preferences

# Register your models here.
admin.site.register(User)
admin.site.register(City)
admin.site.register(Preferences)