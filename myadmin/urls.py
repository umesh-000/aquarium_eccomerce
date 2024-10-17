from django.contrib import admin
from django.urls import path
from myadmin import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('<int:id>/profile_details', views.admin_profile_details, name='admin_profile_details'),
    path('<int:id>/change_password', views.admin_change_password, name='admin_change_password'),

    # Parent Category
    path('p_categories/', views.parent_categories, name='parent_categories_list'),
    path('p_categories/create/', views.parent_categories_create, name='parent_categories_create'),
    path('p_categories/<int:id>/edit', views.parent_categories_edit, name='parent_categories_edit'),
    path('p_categories/<int:id>/delete', views.parent_categories_delete, name='parent_categories_delete'),

    # Category
    path('categories/', views.categories, name='categories_list'),
    path('categories/create/', views.categories_create, name='categories_create'),
    path('categories/<int:id>/edit', views.categories_edit, name='categories_edit'),
    path('categories/<int:id>/delete', views.categories_delete, name='categories_delete'),

    # Products
    path('products/', views.products_list, name='products_list'),
    path('products/create/', views.products_create, name='products_create'),
    path('products/<int:id>/edit', views.products_edit, name='products_edit'),
    path('products/<int:id>/delete', views.products_delete, name='products_delete'),

    # Customers
    path('customers/', views.customers_list, name='customers_list'),
    path('customers/create/', views.customers_create, name='customers_create'),
    path('customers/<int:id>/edit', views.customers_edit, name='customers_edit'),
    path('customers/<int:id>/delete', views.customers_delete, name='customers_delete'),

    # Banners
    path('banners/', views.banners_list, name='banners_list'),
    path('banners/create', views.banner_create, name='banner_create'),
    path('banners/<int:id>/edit', views.banner_edit, name='banner_edit'),
    path('banners/<int:id>/delete', views.banner_delete, name='banner_delete'),
]
