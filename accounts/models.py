from django.db import models

# Create your models here.

class User(models.Model):
    can_add_product = models.BooleanField(default=False)