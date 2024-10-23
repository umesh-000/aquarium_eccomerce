from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db import transaction
from myadmin import models as adminmodel

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

    def get_default_shipping_address(self):
        return self.address_book.filter(address_type='shipping', is_default=True).first()

    def get_default_delivery_address(self):
        return self.address_book.filter(address_type='delivery', is_default=True).first()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.email}"
    

# Customer address book
class AddressBook(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('shipping', 'Shipping'),
        ('delivery', 'Delivery'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='address_book')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default='delivery')
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField( max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'customer_address_book'
        unique_together = ('customer', 'address_type', 'is_default')

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_default:
                AddressBook.objects.filter(customer=self.customer, address_type=self.address_type, is_default=True).update(is_default=False)
            super().save(*args, **kwargs)  

    def __str__(self):
        return f"{self.address_type.capitalize()} address for {self.customer.user.email}"



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
    product = models.ForeignKey(adminmodel.Product, on_delete=models.CASCADE, related_name='wishlists')
    added_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'customer_wishlist'


# Customer Cart
class Cart(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(adminmodel.Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customer_cart'
        unique_together = ('customer', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.customer.user.email}"