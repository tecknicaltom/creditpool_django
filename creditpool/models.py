from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    history_days = models.SmallIntegerField(default=7)

class GlobalTransaction(models.Model):
    creator = models.ForeignKey(User, null=False)
    entered = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    @models.permalink
    def get_absolute_url(self):
        return ('transaction', (), {
            'id': self.pk,
            })

class UserTransaction(models.Model):
    transaction = models.ForeignKey(GlobalTransaction, null=False)
    user = models.ForeignKey(User, null=False)
    credit = models.DecimalField(max_digits=10, decimal_places=2)
    confirmed = models.BooleanField(default=False)
