from django.urls import path
from mysite import views

urlpatterns = [
    path('', views.home, name='site_home'),
    path('about/', views.about, name='about_us'),
    path('contact/', views.contact, name='contact_us'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('user_wishlist/', views.user_wishlist, name='user_wishlist'),
    path('user_address/', views.user_address, name='user_address'),
    path('user_review/', views.user_review, name='user_review'),
    path('user_payment_methods/', views.user_payment_method, name='user_payment_method'),
    path('user_help_topic/', views.user_help_topic, name='user_help_topic'),
    
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),

    path('shop_catalog/', views.shop_catalog, name='shop_catalog'),
    path('product_details/<int:id>/', views.product_details, name='product_details'),
    
    path('category_products/<int:id>/', views.category_products, name='category_products'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('proceed_to_checkout/', views.proceed_to_checkout, name='proceed_to_checkout'),
    path('proceed_to_shipping/', views.proceed_to_shipping, name='proceed_to_shipping'),
    path('proceed_to_payment/', views.proceed_to_payment, name='proceed_to_payment'),


    # AJAX 
    path('update_cart_item/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove_cart_item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('toggle-wishlist/<int:id>/', views.toggle_wishlist, name='toggle_wishlist'),
]