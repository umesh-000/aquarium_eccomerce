from django.urls import path
from mysite import views

urlpatterns = [
    path('', views.home, name='site_home'),
    path('about/', views.about, name='about_us'),
    path('contact/', views.contact, name='contact_us'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),

    path('shop_catalog/', views.shop_catalog, name='shop_catalog'),
    path('product_details/<int:id>/', views.product_details, name='product_details'),
    
    path('category_products/<int:id>/', views.category_products, name='category_products'),
]
