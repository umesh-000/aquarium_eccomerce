# Generated by Django 4.2.16 on 2024-10-15 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customer_wishlist_orderhistory_addressbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='customers/profiles/'),
        ),
    ]
