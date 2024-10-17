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


class ProductTag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Tag Name")
    
    class Meta:
        db_table = 'product_tag'
    
    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    name = models.CharField(max_length=100, verbose_name="Variant Name")  # Example: Color, Size
    value = models.CharField(max_length=100, verbose_name="Variant Value")  # Example: Red, Large

    class Meta:
        db_table = 'products_variant'

    def __str__(self):
        return f"{self.name}: {self.value}"

class ProductVideo(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='videos', verbose_name="Product")
    video = models.FileField(upload_to='products/videos/', verbose_name="Product Video", blank=True, null=True)

    class Meta:
        db_table = 'product_videos'

    def __str__(self):
        return f"Video for {self.product.name}"

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', verbose_name="Product")
    image = models.ImageField(upload_to='products/images/', verbose_name="Product Image")

    class Meta:
        db_table = 'product_images'

    def __str__(self):
        return f"Image for {self.product.name}"

class Product(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]
    FEATURE_CHOICES = [
    (1, 'Related Product'),
    (2, 'Featured Product'),
    (3, 'Popular Product'),
    (4, 'Special Product'),
]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Category")
    name = models.CharField(max_length=255, verbose_name="Product Name")
    description = models.TextField(verbose_name="Product Description", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.PositiveIntegerField(verbose_name="Stock")
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU Number")  # SKU number
    tags = models.ManyToManyField('ProductTag', related_name='products', verbose_name="Tags", blank=True)
    variants = models.ManyToManyField(ProductVariant, related_name='products', verbose_name="Product Variants", blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Status")  # Active/Inactive
    feature = models.IntegerField(choices=FEATURE_CHOICES, default=1, verbose_name="Product Feature")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        db_table = 'products'
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
    

class BannerSlider(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_link = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='banner_images/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        db_table = 'banner_slider'