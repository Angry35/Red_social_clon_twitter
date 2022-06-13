from email.policy import default
from sqlite3 import Timestamp
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(default='hola, twitter',max_length= 100)
    # habilitamos las imagenes
    image = models.ImageField(default='default.png')
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
    #creamos una funcion para obtener la cuenta de los usurios que tienen relaciones
    
    def following (self):
        user_ids = Relationship.objects.filter(from_user= self.user)\
                                   .values_list('to_user_id',flat =True)
        return User.objects.filter(id__in=user_ids)
    def followers (self):
        user_ids = Relationship.objects.filter(to_user= self.user)\
                                   .values_list('from_user_id',flat =True)
        return User.objects.filter(id__in=user_ids)

class Post(models.Model):
    Timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    class meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return self.content
class Relationship(models.Model):
    from_user = models.ForeignKey(User,related_name='relationships',on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,related_name='related_to',on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.from_user} to {self.to_user}'
    
    