from django.contrib import admin
from django.urls import path
from myadmin import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),

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
]
