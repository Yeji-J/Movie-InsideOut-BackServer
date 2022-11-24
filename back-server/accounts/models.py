from django.db import models
from django.contrib.auth.models import AbstractUser
    
def profile_image_path(instance, filename):
    return f'profile/{instance.username}/{filename}'

class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='follower')
    profile_image = models.ImageField(default='/profile/default.png', blank=True, upload_to=profile_image_path)