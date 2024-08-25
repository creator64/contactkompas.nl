from django.db import models


class Bedrijf(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    image_url = models.CharField(max_length=200, null=True)
    popularity = models.IntegerField(db_index=True, null=True)
