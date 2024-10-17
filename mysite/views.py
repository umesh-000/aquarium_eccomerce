from django.core.paginator import Paginator
from myadmin import models as adminmodels
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.db.models import Q

def home(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)  # Count products related to subcategories
    ).prefetch_related('categories')  # Prefetch categories to avoid additional queries
    # Fetch all active products

    banners = adminmodels.BannerSlider.objects.filter(is_active=True)[:3]

    popular_products = adminmodels.Product.objects.filter(status=1,feature=3)
    special_products = adminmodels.Product.objects.filter(status=1, feature=4).order_by('-created_at')[:4]
    context = {
        'p_categories': p_categories,
        'popular_products' :popular_products,
        'special_products' :special_products,
        'banners': banners,
    }
    return render(request, 'mysite/index.html', context)


def about(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)  # Count products related to subcategories
    ).prefetch_related('categories')  # Prefetch categories to avoid additional queries
    context = {
        'p_categories': p_categories,
    }
    return render(request, 'mysite/about_us.html',context)


def contact(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)  # Count products related to subcategories
    ).prefetch_related('categories')  # Prefetch categories to avoid additional queries
    context = {
        'p_categories': p_categories,
    }
    return render(request, 'mysite/contact_us.html', context)


def terms_conditions(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)  # Count products related to subcategories
    ).prefetch_related('categories')  # Prefetch categories to avoid additional queries
    context = {
        'p_categories': p_categories,
    }
    return render(request, 'mysite/terms_and_conditions.html', context)


def shop_catalog(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)
    ).prefetch_related('categories')

    # Get all active products
    product_list = adminmodels.Product.objects.filter(status=1)

    # Count total products
    total_products = product_list.count()

    # Paginate products (4 products per page)
    paginator = Paginator(product_list, 8)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'p_categories': p_categories,
        'products': products,
        'total_products': total_products,
    }
    return render(request, 'mysite/shop_catalog.html', context)


def product_details(request, id):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)
    ).prefetch_related('categories')
    product = get_object_or_404(adminmodels.Product, id=id)
    product_images = product.images.all()

    context = {
        'product': product,
        'product_images': product_images,
        'p_categories': p_categories,
    }
    return render(request, 'mysite/product_details.html', context)


def category_products(request, id):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)
    ).prefetch_related('categories')
    parent_category = get_object_or_404(adminmodels.ParentCategory, id=id)
    subcategories = adminmodels.Category.objects.filter(parent_category=parent_category)
    products = adminmodels.Product.objects.filter( Q(category__in=subcategories) & Q(status=1) )
    total_products = products.count()
    # Paginate products (8 products per page)
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'parent_category':parent_category,
        'p_categories': p_categories,
        'subcategories': subcategories,
        'products': products,
        'total_products': total_products,
    }
    return render(request, 'mysite/category_products.html', context)

