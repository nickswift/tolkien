from django.db import models


# User authentication metadata fingerprint
class TUserMeta(models.Model):
    avg_attempts = models.IntegerField(default=0)
    avg_keystrokes = models.IntegerField(default=0)
    avg_backspaces = models.IntegerField(default=0)


# Tolkien Authentication information tables
class TUser(models.Model):
    username = models.CharField(max_length=64)
    passwd_digest = models.CharField(max_length=60)
    metadata = models.OneToOneField(TUserMeta, related_name='owner')