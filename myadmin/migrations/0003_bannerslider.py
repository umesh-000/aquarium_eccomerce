# Generated by Django 4.2.16 on 2024-10-17 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_product_feature'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('button_text', models.CharField(blank=True, max_length=50, null=True)),
                ('button_link', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='banner_images/')),
                ('order', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'banner_slider',
                'ordering': ['order'],
            },
        ),
    ]
