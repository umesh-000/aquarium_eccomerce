from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Extending the User model
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    class Meta:
        db_table = 'accounts_user'

class Admins(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='admin/profiles/', blank=True, null=True)
    class Meta:
        db_table = 'admins'