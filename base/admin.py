from django.contrib import admin
from .models import Room,Topic, Message,User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)