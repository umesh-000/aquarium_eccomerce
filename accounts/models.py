from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


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




# Extending the User model for customers
class Customer(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_profile')
    profile_image = models.ImageField(upload_to='customers/profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="Status")  
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.email}"

# Customer address book
class AddressBook(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='address_book')
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'customer_address_book'

# Customer order history
class OrderHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order_history')
    order_number = models.CharField(max_length=100)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'customer_order_history'

# Customer wishlist
class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlist')
    product_name = models.CharField(max_length=255)
    added_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'customer_wishlist'