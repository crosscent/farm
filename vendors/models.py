from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # This line is required.  Links UserProfile to a User model instance.

    # The additional attributes we wish to include.
    location = models.CharField(max_length=100)
    position = models.IntegerField(null=True)
    company = models.CharField(max_length=100)
    map_lon = models.FloatField(null=True)
    map_lat = models.FloatField(null=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username