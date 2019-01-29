from django.db import models
from django.conf import settings
from django.urls import reverse

from restaurants.models import RestaurantLocation


# Create your models here.
class Item(models.Model):
    # Associations
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(RestaurantLocation, on_delete=models.CASCADE)
    # item stuff
    name = models.CharField(max_length=120)
    contents = models.TextField(help_text="Separate each item by comma")
    excludes = models.TextField(blank=True, null=True, help_text="Separate each item by comma")
    public = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menus:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-updated', '-created']

    def get_contents(self):
        return self.contents.split(",")

    def get_excludes(self):
        return self.excludes.split(",")
