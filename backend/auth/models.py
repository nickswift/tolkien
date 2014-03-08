from django.db import models

# Tolkien Authentication information tables
class AuthUser(models.Model):
    username = models.CharField(max_length=64)
    passwd_digest = models.CharField(max_length=60)

# User authentication metadata fingerprint
class UserMeta(models.Model):
    owner  = models.ForeignKey(AuthUser)
    values = models.TextField()

# Login session -- making this bare-bones, because it's not the focus of the
# project
class UserSession(models.Model):
    ticket_holder = models.OneToOneField(AuthUser, primary_key=True)
    session_token = models.CharField(max_length=32, unique=True)
    expiry        = models.DateTimeField()