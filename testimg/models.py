from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
import os

# Create your models here.

# User CLass for user,username and userimg path

class User(AbstractUser):
	like_list = models.CharField(max_length=100, default='', blank=True)
	labels = models.CharField(max_length=100, default='', blank=True)
	current_visiting_path = models.CharField(max_length=100, default='')


def get_image_path(instance, filename):
	return os.path.join('photos', filename).replace('\\','/')

class ImageData(models.Model):
	image = models.ImageField(upload_to = get_image_path)
	username = models.ForeignKey('User')
	path = models.CharField(max_length=1024, default='')
	likes = models.IntegerField(default = 0)
	created_at = models.DateTimeField(default = timezone.now)
	img_labels = models.CharField(max_length = 100, default = '', blank = True)
	feature = models.TextField(blank = True, null = True)