from django.db import models

class ParentCategory(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]
    name = models.CharField(max_length=255, verbose_name="Category Name")
    image = models.ImageField(upload_to='categories/parent_category/', verbose_name="Category Image")
    description = models.TextField(verbose_name="Category Description")
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        db_table = 'parent_categories'    
        verbose_name = "Parent Category"
        verbose_name_plural = "Parent Categories"


    def __str__(self):
        return self.name
    

class Category(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]
    parent_category = models.ForeignKey(ParentCategory, on_delete=models.CASCADE, related_name='categories', verbose_name="Parent Category")  # Foreign key to ParentCategory
    name = models.CharField(max_length=255, verbose_name="Category Name")
    image = models.ImageField(upload_to='categories/category/', verbose_name="Category Image", blank=True, null=True)
    description = models.TextField(verbose_name="Category Description", default="")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        db_table = 'categories'
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name