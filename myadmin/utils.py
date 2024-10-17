from myadmin import models
import random

def generate_unique_sku(prefix='SKU', length=8):
    """Generate a unique SKU with the given prefix and an 8-digit number."""
    while True:
        number = str(random.randint(10000000, 99999999))
        sku = f"{prefix}{number}"
        # Check if this SKU already exists
        if not models.Product.objects.filter(sku=sku).exists():
            return sku