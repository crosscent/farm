__author__ = 'Roy'

from django.contrib import admin
from list.models import Category, Product

admin.site.register(Category)
admin.site.register(Product)