from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class UserTransfer(models.Model):
	user = models.ForeignKey(User, null=False)
	credit = models.DecimalField(max_digits=10, decimal_places=2)
	entered = models.DateTimeField(auto_now_add=True)
	confirmed = models.BooleanField()

class GlobalTransfer(models.Model):
	creator = models.ForeignKey(User)
	date = models.DateField(null=False)
	entered = models.DateTimeField(auto_now_add=True)
	description = models.TextField()


