from django.db import models


# Create your models here.


class User(models.Model):
    uid = models.CharField(max_length=20, unique=True)
    password = models.TextField()

    class Mate:
        db_table = 'user'

