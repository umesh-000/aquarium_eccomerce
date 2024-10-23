from django.core.paginator import Paginator
from myadmin import models as adminmodels
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts import models as accountmMdels
from django.http import JsonResponse
from django.contrib import messages
import json


def custom_404(request, exception):
    return render(request, 'mysite/page404.html', status=404)


def home(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)  # Count products related to subcategories
    ).prefetch_related('categories')  # Prefetch categories to avoid additional queries
    # Fetch all active products
    banners = adminmodels.BannerSlider.objects.filter(is_active=True)[:3]
    popular_products = adminmodels.Product.objects.filter(status=1,feature=3)
    special_products = adminmodels.Product.objects.filter(status=1, feature=4).order_by('-created_at')[:4]
    wishlist_products = accountmMdels.Wishlist.objects.filter(customer__user=request.user).values_list('product_id', flat=True) if request.user.is_authenticated else []

    for product in popular_products:
        product.is_in_wishlist = product.id in wishlist_products

    for product in special_products:
        product.is_in_wishlist = product.id in wishlist_products

    cart_item_count = 0
    cart_item_count
    cart_products = []
    total_price = 0


    if request.user.is_authenticated:
        # Get the logged-in user's customer profile
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        total_price = sum(item.product.price * item.quantity for item in cart_products)

    context = {
        'p_categories': p_categories,
        'popular_products' :popular_products,
        'special_products' :special_products,
        'banners': banners,
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'mysite/index.html', context)

@csrf_protect
def update_cart_item(request, cart_item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        new_quantity = data.get('quantity')
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=403)
        cart_item = get_object_or_404(accountmMdels.Cart, id=cart_item_id, customer__user=request.user)
        if new_quantity is not None and new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            return JsonResponse({'message': 'Quantity updated successfully!'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_protect
def remove_cart_item(request, cart_item_id):
    if request.method == 'DELETE':
        cart_item = get_object_or_404(accountmMdels.Cart, id=cart_item_id)
        cart_item.delete()
        return JsonResponse({'message': 'Item removed from cart'}, status=204)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def toggle_wishlist(request, id):
    if request.method == 'POST':
        product = get_object_or_404(adminmodels.Product, id=id)
        customer = get_object_or_404(accountmMdels.Customer, user=request.user)
        wishlist_item, created = accountmMdels.Wishlist.objects.get_or_create(customer=customer, product=product)
        if created:
            return JsonResponse({'status': 'added'})
        else:
            wishlist_item.delete()
            return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'error'}, status=400)


def about(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)  # Count products related to subcategories
    ).prefetch_related('categories')  # Prefetch categories to avoid additional queries
    cart_item_count = 0
    cart_products = []

    if request.user.is_authenticated:
        # Get the logged-in user's customer profile
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')

    context = {
        'p_categories': p_categories,
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
    }
    return render(request, 'mysite/about_us.html',context)

def contact(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate( total_products=Count('categories__products', distinct=True) ).prefetch_related('categories') 
    cart_item_count = 0
    total_price = 0
    cart_products = []

    if request.user.is_authenticated:
        # Get the logged-in user's customer profile
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        total_price = sum(item.product.price * item.quantity for item in cart_products)

    context = {
        'p_categories': p_categories,
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'mysite/contact_us.html', context)

def user_dashboard(request):
    cart_item_count = 0
    total_price = 0
    cart_products = []
    if request.user.is_authenticated:
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate( total_products=Count('categories__products', distinct=True) ).prefetch_related('categories')
        total_price = sum(item.product.price * item.quantity for item in cart_products)
        context = {
            'cart_item_count': cart_item_count,
            'cart_products': cart_products,
            'p_categories': p_categories,
            'total_price': total_price,
            }
        return render(request, 'mysite/user_dashboard.html', context)
    
def user_orders(request):
    cart_item_count = 0
    total_price = 0
    cart_products = []
    if request.user.is_authenticated:
        customer = accountmMdels.Customer.objects.get(user=request.user)
        orders = accountmMdels.OrderHistory.objects.filter(customer=customer).select_related('product').order_by('-order_date')
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate( total_products=Count('categories__products', distinct=True) ).prefetch_related('categories')
        total_price = sum(item.product.price * item.quantity for item in cart_products)
      
        context = {
            'orders': orders,
            'cart_item_count': cart_item_count,
            'cart_products': cart_products,
            'p_categories': p_categories,
            'total_price': total_price,
            }
        return render(request, 'mysite/user_orders.html', context)       

def user_wishlist(request):
    cart_item_count = 0
    total_price = 0
    cart_products = []
    if request.user.is_authenticated:
        customer = get_object_or_404(accountmMdels.Customer, user=request.user)
        wishlist = accountmMdels.Wishlist.objects.filter(customer=customer).select_related('product').order_by('-added_date')
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(total_products=Count('categories__products', distinct=True)).prefetch_related('categories')
        total_price = sum(item.product.price * item.quantity for item in cart_products)
        context = {
            'wishlist': wishlist,
            'cart_item_count': cart_item_count,
            'cart_products': cart_products,
            'p_categories': p_categories,
            'total_price': total_price,
        }
        return render(request, 'mysite/user_wishlist.html', context)
    else:
        return redirect('login')



@login_required
def user_address(request):
    cart_item_count = 0
    total_price = 0
    cart_products = []
    user_addresses = [] 
    
    if request.user.is_authenticated:
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
            total_products=Count('categories__products', distinct=True)
        ).prefetch_related('categories')
        total_price = sum(item.product.price * item.quantity for item in cart_products)
        # Fetch all addresses for the user
        user_addresses = accountmMdels.AddressBook.objects.filter(customer=customer)

    if request.method == 'POST':
        address_type = request.POST.get('address_type')
        country = request.POST.get('country')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2', '') 
        default_adrs = request.POST.get('default_adrs') == 'on'

        address = accountmMdels.AddressBook.objects.create(
            customer=customer,
            address_type=address_type,
            country=country,
            city=city,
            state=state,
            postal_code=postal_code,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            is_default=default_adrs,
        )
        messages.success(request, 'Address added successfully!')

    context = {
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
        'p_categories': p_categories,
        'total_price': total_price,
        'user_addresses': user_addresses,  
        'customer':customer,
    }
    return render(request, 'mysite/user_address.html', context)


def user_review(request):
    cart_item_count = 0
    total_price = 0
    cart_products = []
    if request.user.is_authenticated:
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate( total_products=Count('categories__products', distinct=True) ).prefetch_related('categories')
        total_price = sum(item.product.price * item.quantity for item in cart_products)
        context = {
            'cart_item_count': cart_item_count,
            'cart_products': cart_products,
            'p_categories': p_categories,
            'total_price': total_price,
            }
    return render(request, 'mysite/user_review.html', context)

def user_payment_method(request):
    cart_item_count = 0
    total_price = 0
    cart_products = []
    if request.user.is_authenticated:
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate( total_products=Count('categories__products', distinct=True) ).prefetch_related('categories')
        total_price = sum(item.product.price * item.quantity for item in cart_products)
        context = {
            'cart_item_count': cart_item_count,
            'cart_products': cart_products,
            'p_categories': p_categories,
            'total_price': total_price,
            }
    return render(request, 'mysite/user_payment_method.html', context)

def user_help_topic(request):
    cart_item_count = 0
    total_price = 0
    cart_products = []
    if request.user.is_authenticated:
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate( total_products=Count('categories__products', distinct=True) ).prefetch_related('categories')
        total_price = sum(item.product.price * item.quantity for item in cart_products)
        context = {
            'cart_item_count': cart_item_count,
            'cart_products': cart_products,
            'p_categories': p_categories,
            'total_price': total_price,
            }
    return render(request, 'mysite/user_help_topics.html', context)           


def terms_conditions(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)  # Count products related to subcategories
    ).prefetch_related('categories')  # Prefetch categories to avoid additional queries
    cart_item_count = 0
    total_price = 0
    cart_products = []

    if request.user.is_authenticated:
        # Get the logged-in user's customer profile
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        total_price = sum(item.product.price * item.quantity for item in cart_products)

    context = {
        'p_categories': p_categories,
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'mysite/terms_and_conditions.html', context)


def shop_catalog(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)
    ).prefetch_related('categories')

    cart_item_count = 0
    cart_products = []
    total_price = 0

    product_list = adminmodels.Product.objects.filter(status=1)

    if request.user.is_authenticated:
        # Get the logged-in user's customer profile
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        wishlist_products = accountmMdels.Wishlist.objects.filter(customer__user=request.user).values_list('product_id', flat=True) if request.user.is_authenticated else []
        for product in product_list:
            product.is_in_wishlist = product.id in wishlist_products
    
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
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
    }
    return render(request, 'mysite/shop_catalog.html', context)


def product_details(request, id):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)
    ).prefetch_related('categories')
    product = get_object_or_404(adminmodels.Product, id=id)
    product_images = product.images.all()
    cart_item_count = 0
    cart_products = []
    total_price = 0

    if request.user.is_authenticated:
        # Get the logged-in user's customer profile
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        total_price = sum(item.product.price * item.quantity for item in cart_products)

    context = {
        'product': product,
        'product_images': product_images,
        'p_categories': p_categories,
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
        'total_price': total_price,
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

    cart_item_count = 0
    cart_products = []
    total_price = 0

    if request.user.is_authenticated:
        # Get the logged-in user's customer profile
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        total_price = sum(item.product.price * item.quantity for item in cart_products)

    context = {
        'parent_category':parent_category,
        'p_categories': p_categories,
        'subcategories': subcategories,
        'products': products,
        'total_products': total_products,
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'mysite/category_products.html', context)


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(adminmodels.Product, id=product_id)
        if request.user.is_authenticated:
            customer = get_object_or_404(accountmMdels.Customer, user=request.user)
            cart_item, created = accountmMdels.Cart.objects.get_or_create(
                customer=customer,
                product=product,
                defaults={'quantity': 1}
            )
            if created:
                messages.success(request, 'Product added to cart successfully.')
            else:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, 'Product quantity updated in cart.')
            return JsonResponse({'success': True, 'message': 'Product added to cart successfully.'})
        else:
            messages.error(request, 'You need to log in to add items to your cart.')
            return JsonResponse({'success': False, 'message': 'User not authenticated.', 'redirect_url': '/mysite/login/'})
    messages.error(request, 'Invalid request method.')
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def view_cart(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)
    ).prefetch_related('categories')

    cart_item_count = 0
    cart_products = []
    total_price = 0

    if request.user.is_authenticated:
        # Get the logged-in user's customer profile
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        total_price = sum(item.product.price * item.quantity for item in cart_products)
     
    context={
        'p_categories': p_categories,
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'mysite/view_cart.html', context)


def proceed_to_checkout(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)
    ).prefetch_related('categories')

    cart_item_count = 0
    total_price = 0
    cart_products = []

    if request.user.is_authenticated:
        # Get the logged-in user's customer profile
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        total_price = sum(item.product.price * item.quantity for item in cart_products)

    context={
        'p_categories': p_categories,
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'mysite/proceed_to_checkout.html', context)


def proceed_to_shipping(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)
    ).prefetch_related('categories')

    cart_item_count = 0
    total_price = 0
    cart_products = []

    if request.user.is_authenticated:
        # Get the logged-in user's customer profile
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        total_price = sum(item.product.price * item.quantity for item in cart_products)

    context={
        'p_categories': p_categories,
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'mysite/proceed_to_shipping.html', context)

def proceed_to_payment(request):
    p_categories = adminmodels.ParentCategory.objects.filter(status=1).annotate(
        total_products=Count('categories__products', distinct=True)
    ).prefetch_related('categories')

    cart_item_count = 0
    total_price = 0
    cart_products = []

    if request.user.is_authenticated:
        # Get the logged-in user's customer profile
        customer = accountmMdels.Customer.objects.get(user=request.user)
        cart_item_count = accountmMdels.Cart.objects.filter(customer=customer).count()
        cart_products = accountmMdels.Cart.objects.filter(customer=customer).select_related('product')
        total_price = sum(item.product.price * item.quantity for item in cart_products)

    context={
        'p_categories': p_categories,
        'cart_item_count': cart_item_count,
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, 'mysite/proceed_to_payment.html', context)