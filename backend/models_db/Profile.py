from django.db import models


class Profile(models.Model):
    username = models.CharField(unique=True, max_length=30, primary_key=True)
    password = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'User'
