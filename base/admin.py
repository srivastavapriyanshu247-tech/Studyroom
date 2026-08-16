from django.contrib import admin

# Register your models here.
from .models import Room,topic,message,User
admin.site.register(User)
admin.site.register(Room)
admin.site.register(topic)
admin.site.register(message)