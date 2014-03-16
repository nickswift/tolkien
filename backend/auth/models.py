from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserMeta(models.Model):
	owner = models.OneToOneField(User, primary_key=True)
	data = models.TextField()