from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    pic = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    def __unicode__(self):
        return unicode(self.name)

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    location = models.CharField(max_length=100)
    pic = models.CharField(max_length=100)
