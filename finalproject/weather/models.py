from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class User(AbstractUser):
    pass

class City(models.Model):
	id = models.IntegerField(primary_key=True)
	lat = models.FloatField()
	lon = models.FloatField()
	name = models.CharField(max_length=64)
	country = models.CharField(max_length=64)
	favs = models.ManyToManyField("User", related_name="cities", blank=True)

class Preferences(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	unitchoices = [("Standard", "Standard"), ("Metric", "Metric"), ("Imperial", "Imperial")]
	unit = models.CharField("Unit:", max_length=64, choices=unitchoices, default=unitchoices[0][0])

	@receiver(post_save, sender=User)
	def create_user_preferences(sender, instance, created, **kwargs):
		if created:
			Preferences.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_preferences(sender, instance, **kwargs):
		instance.preferences.save()