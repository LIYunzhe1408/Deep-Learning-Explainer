from django.db import models


# Create your models here.
class User(models.Model):
    ID = models.BigIntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    institution = models.CharField(max_length=50)
    permission = models.CharField(max_length=20)
    password = models.CharField(max_length=12)
    loggedIn = models.CharField(max_length=1)
    picture = models.CharField(max_length=255)


class Log(models.Model):
    ID = models.IntegerField()
    update_time = models.DateTimeField()
    user_name = models.CharField(max_length=255)
    change_log = models.CharField(max_length=255)