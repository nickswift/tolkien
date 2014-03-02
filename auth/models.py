from django.db import models

# Tolkien Authentication information tables
class AuthUser(models.Model):
    username = models.CharField(max_length=64)
    passwd_digest = models.CharField(max_length=60)

# User authentication metadata fingerprint
class AuthMeta(models.Model):
    owner        = models.ForeignKey(AuthUser)
    avg_attempts = models.IntegerField(default=0)
    avg_keystrokes = models.IntegerField(default=0)
    avg_backspaces = models.IntegerField(default=0)
    