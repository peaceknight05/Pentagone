from django.db import models

# Create your models here.


class Deck(models.Model):
    name = models.CharField(max_length=100)
    data = models.JSONField(null=True, blank=True)
    cache = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Name: {self.name}, {len(self.data['words'])} cards"


class OldDeck(models.Model):
    words = models.JSONField(null=True, blank=True)
    cache = models.JSONField(null=True, blank=True)


class Card(models.Model):
    term = models.CharField(max_length=100)
    definition = models.CharField(max_length=100)
    timestamp = models.IntegerField(default=0)
    maxtimesince = models.IntegerField(default=0)
    lasttimesince = models.IntegerField(default=0)
    right = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    lasteval = models.IntegerField(default=0)
