from django.db import models
from django.contrib.auth.models import User


# user models here
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.TextField(blank=True,null=True)
    phone = models.IntegerField(blank=True,null=True)
    bio = models.TextField()
    def __str__(self):
        return self.user.username