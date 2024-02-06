from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="https://res.cloudinary.com/dtostqvav/image/upload/v1707223140/kgeg16zar09uqry5xdh6.svg",upload_to='discord_user_dp')
    followers = models.ManyToManyField("self", symmetrical=False, related_name="users_following", blank=True)
    following = models.ManyToManyField("self", symmetrical=False, related_name="users_followed_by", blank=True)
    
    def __str__(self):
        return self.username   
    
    
class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL, null= True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null= True)
    participants = models.ManyToManyField(User, related_name="participants", blank= True,)
    name = models.CharField(max_length= 250)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-updated", "-created"]

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE,) # CASCADE means will delete after the room has been deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]