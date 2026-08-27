from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name=models.CharField(max_length=200,null=True)
    bio=models.TextField(null=True)
    email=models.CharField(unique=True)
    avatar=models.ImageField(null=True,default='avatar.svg')
    followers=models.ManyToManyField('self',related_name='following',symmetrical=False,blank=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

class topic(models.Model):
    name=models.CharField(max_length=150)

    def __str__(self):
        return self.name
class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=150)
    description=models.TextField(null=True,blank=True)
    members=models.ManyToManyField(User,related_name='member',blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return self.name

class message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.SET_NULL,null=True)
    body=models.TextField()
    edit=models.BooleanField(default=False)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return self.body[0:50]

