from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField( max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null= True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
class Topic(models.Model):
    name = models.CharField(_("name"), max_length=200)
    class Meta:
        
        verbose_name = 'topic'
        verbose_name_plural = 'topics'
    
    def __str__(self):
        return self.name
class Room(models.Model):
    host = models.ForeignKey(User, verbose_name=_("host"), on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey("base.Topic", verbose_name=_("topic"), on_delete=models.SET_NULL, null=True)
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"), null=True, blank=True)
    participant = models.ManyToManyField(User, related_name="participant" , verbose_name=_("participants"))
    updated = models.DateTimeField(_("update"), auto_now=True)
    created = models.DateTimeField(_("create"), auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Room'
        verbose_name = 'room'
        verbose_name_plural = 'rooms'
        ordering = ["-updated","-created"]
class Message(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    room = models.ForeignKey("base.Room", verbose_name=_("room"), on_delete=models.CASCADE)
    body = models.TextField(_("body"))
    updated = models.DateTimeField(_("update"), auto_now=True)
    created = models.DateTimeField(_("create"), auto_now_add=True)
    class Meta:
        ordering = ["-updated","-created"]


    def __str__(self):
        return self.body[:50]