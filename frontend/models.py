from django.db import models

# Create your models here.


class Deck(models.Model):
    words = models.JSONField()
    cache = models.JSONField()
    threshold = models.DecimalField(max_digits=2, decimal_places=1)
