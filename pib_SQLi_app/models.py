from django.db import models

# Create your models here.


class Product(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
