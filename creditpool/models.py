from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class GlobalTransfer(models.Model):
	creator = models.ForeignKey(User, null=False)
	entered = models.DateTimeField(auto_now_add=True)
	description = models.TextField()

class UserTransfer(models.Model):
	transfer = models.ForeignKey(GlobalTransfer, null=False)
	user = models.ForeignKey(User, null=False)
	credit = models.DecimalField(max_digits=10, decimal_places=2)
	confirmed = models.BooleanField(default=False)


