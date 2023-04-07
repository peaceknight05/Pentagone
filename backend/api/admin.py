from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.OldDeck)
admin.site.register(models.Deck)
admin.site.register(models.Card)
