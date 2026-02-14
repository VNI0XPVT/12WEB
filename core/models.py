
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Profile(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 wallet_balance = models.IntegerField(default=0)
 subscription_expiry = models.DateTimeField(null=True, blank=True)
 otp = models.CharField(max_length=6, blank=True)

 def is_active(self):
  return self.subscription_expiry and self.subscription_expiry > timezone.now()
