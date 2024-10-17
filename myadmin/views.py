from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from accounts import models as  account_models
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from myadmin import models
from myadmin import utils
import logging

# Set up logging
logger = logging.getLogger(__name__)

User = get_user_model()  # Get the custom user model

def admin_dashboard(request):
    # Check if the user session exists (handled by middleware)
    if not request.admin_user:
        return redirect('login')

    context = {
        'admin_user': request.admin_user,
    }
    return render(request, 'admin/dashboard.html',context)

def admin_profile_details(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    admin_profile = get_object_or_404(account_models.Admins, id=id)
    
    context = {
        'admin_user': request.user,
        'admin_profile': admin_profile,
    }
    return render(request, 'admin/admin_profile.html',context)

def admin_change_password(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    admin_profile = get_object_or_404(account_models.Admins, id=id)
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        user = admin_profile.user
        # Check if the current password is correct
        if not check_password(current_password, user.password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('admin_profile_details', id=id)

        # Check if new passwords match
        if new_password != confirm_new_password:
            messages.error(request, 'New password and confirmation do not match.')
            return redirect('admin_profile_details', id=id)

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Update session so the user isn't logged out
        update_session_auth_hash(request, user)

        messages.success(request, 'Password updated successfully.')
        return redirect('admin_profile_details', id=id)

    context = {
        'admin_user': request.user,
        'admin_profile': admin_profile,
    }
    return render(request, 'admin/admin_profile.html', context)



def parent_categories(request):
    if not request.admin_user:
        return redirect('login')
    categories = models.ParentCategory.objects.all()
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'admin_user': request.admin_user,
        'parent_categories': page_obj,
    }
    
    return render(request, 'admin/parent_categories_list.html', context)

def parent_categories_create(request):
    if not request.admin_user:
        return redirect('login')
    
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        image = request.FILES.get('file')
        
        # Create the category
        try:
            parent_category = models.ParentCategory.objects.create(
                name=name,
                description=description,
                status=status,
                image=image,
            )
            messages.success(request, 'Category created successfully!')
            return redirect('parent_categories_list')
        except Exception as e:
            messages.error(request, f'Error creating category: {str(e)}')
    
    context = {
        'admin_user': request.admin_user,
    }
    return render(request, 'admin/parent_categories_create.html', context)

def parent_categories_edit(request, id):
    if not request.admin_user:
        return redirect('login')

    parent_category = get_object_or_404(models.ParentCategory, id=id)

    if request.method == 'POST':
        # Handle form submission
        parent_category.name = request.POST.get('title')
        parent_category.status = request.POST.get('status')
        parent_category.description = request.POST.get('description')

        # Handle file upload if a new file is provided
        if request.FILES.get('file'):
            parent_category.image = request.FILES['file'] 

        parent_category.save()
        messages.success(request, 'Category Updated successfully!')
        return redirect('parent_categories_list')

    context = {
        'admin_user': request.admin_user,
        'parent_category': parent_category,
    }
    return render(request, 'admin/parent_categories_edit.html', context)

def parent_categories_delete(request, id):
    if request.method == 'POST':
        try:
            if not request.admin_user:
                return redirect('login')
            parent_category = get_object_or_404(models.ParentCategory, id=id)
            parent_category.delete()
            return JsonResponse({'success': True, 'message': 'Deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def categories(request):
    if not request.admin_user:
        return redirect('login')
    categories = models.Category.objects.all()
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'admin_user': request.admin_user,
        'categories': page_obj,
    }
    
    return render(request, 'admin/categories_list.html', context)

def categories_create(request):
    if not request.admin_user:
        return redirect('login')
    
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        image = request.FILES.get('file')
        parent_id = request.POST.get('p_id')
        p_cat = get_object_or_404(models.ParentCategory, id=parent_id)
        # Create the category
        try:
            category = models.Category.objects.create(
                name=name,
                description=description,
                status=status,
                image=image,
                parent_category=p_cat,
            )
            messages.success(request, 'Category created successfully!')
            return redirect('categories_list')
        except Exception as e:
            messages.error(request, f'Error creating category: {str(e)}')
    
    context = {
        'admin_user': request.admin_user,
        'parent_categories': models.ParentCategory.objects.all()
    }
    return render(request, 'admin/categories_create.html', context)

def categories_edit(request, id):
    if not request.admin_user:
        return redirect('login')

    category = get_object_or_404(models.Category, id=id)

    if request.method == 'POST':
        # Handle form submission
        category.name = request.POST.get('title')
        category.status = request.POST.get('status')
        category.description = request.POST.get('description')
        id = request.POST.get('p_id')
        p_cat = get_object_or_404(models.ParentCategory, id=id)
        category.parent_category = p_cat

        # Handle file upload if a new file is provided
        if request.FILES.get('file'):
            category.image = request.FILES['file'] 

        category.save()
        messages.success(request, 'Category Updated successfully!')
        return redirect('categories_list')

    context = {
        'admin_user': request.admin_user,
        'category': category,
        'parent_categories': models.ParentCategory.objects.all()
        
    }
    return render(request, 'admin/categories_edit.html', context)

def categories_delete(request, id):
    if request.method == 'POST':
        try:
            if not request.admin_user:
                return redirect('login')
            category = get_object_or_404(models.Category, id=id)
            category.delete()
            return JsonResponse({'success': True, 'message': 'Deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def products_list(request):
    if not request.admin_user:
        return redirect('login')
    
    products = models.Product.objects.all()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'admin_user': request.admin_user,
        'products': page_obj,
    }
    return render(request, 'admin/products_list.html', context)

def products_create(request):
    if not request.admin_user:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')  
        status = request.POST.get('status')
        feature = request.POST.get('feature')
        category_id = request.POST.get('category_id')
        category = get_object_or_404(models.Category, id=category_id)

        # Get related fields like tags, variants
        tags_ids = request.POST.getlist('tags')
        variant_ids = request.POST.getlist('variants')

        # Images and Videos
        images = request.FILES.getlist('images')
        videos = request.FILES.getlist('videos')

        # Generate a unique SKU
        sku = utils.generate_unique_sku()

        # Create the product
        try:
            product = models.Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock=stock,
                sku=sku,  # Using the generated SKU
                status=status,
                feature=feature,
                category=category
            )

            # Attach tags
            if tags_ids:
                product.tags.set(tags_ids)

            # Attach variants
            if variant_ids:
                product.variants.set(variant_ids)

            # Save product images
            for image in images:
                models.ProductImage.objects.create(product=product, image=image)

            # Save product videos
            for video in videos:
                models.ProductVideo.objects.create(product=product, video=video)

            messages.success(request, 'Product created successfully!')
            return redirect('products_list')

        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')

    context = {
        'admin_user': request.admin_user,
        'categories': models.Category.objects.all(),
        'tags': models.ProductTag.objects.all(),
        'variants': models.ProductVariant.objects.all(),
    }
    return render(request, 'admin/products_create.html', context)

def products_edit(request, id):
    if not request.admin_user:
        return redirect('login')

    product = get_object_or_404(models.Product, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        status = request.POST.get('status')
        feature = request.POST.get('feature')
        category_id = request.POST.get('category_id')
        category = get_object_or_404(models.Category, id=category_id)

        # Get related fields like tags, variants
        tags_ids = request.POST.getlist('tags')
        variant_ids = request.POST.getlist('variants')

        # Images and Videos
        images = request.FILES.getlist('images')
        videos = request.FILES.getlist('videos')

        # Update the product details
        try:
            product.name = name
            product.description = description
            product.price = price
            product.stock = stock
            product.status = status
            product.feature=feature
            product.category = category
            product.save()

            # Update tags
            if tags_ids:
                product.tags.set(tags_ids)
            else:
                product.tags.clear()

            # Update variants
            if variant_ids:
                product.variants.set(variant_ids)
            else:
                product.variants.clear()

            # Update images
            if images:
                product.images.all().delete()  # Remove old images
                for image in images:
                    models.ProductImage.objects.create(product=product, image=image)

            # Update videos
            if videos:
                product.videos.all().delete()  # Remove old videos
                for video in videos:
                    models.ProductVideo.objects.create(product=product, video=video)

            messages.success(request, 'Product updated successfully!')
            return redirect('products_list')

        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')

    context = {
        'admin_user': request.admin_user,
        'product': product,
        'categories': models.Category.objects.all(),
        'tags': models.ProductTag.objects.all(),
        'variants': models.ProductVariant.objects.all(),
        'existing_tags': product.tags.values_list('id', flat=True),
        'existing_variants': product.variants.values_list('id', flat=True),
    }
    return render(request, 'admin/products_edit.html', context)

def products_delete(request, id):
    if request.method == 'POST':
        try:
            if not request.admin_user:
                return redirect('login')
            product = get_object_or_404(models.Product, id=id)
            product.delete()
            return JsonResponse({'success': True, 'message': 'Deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



def customers_list(request):
    if not request.user.is_authenticated or request.user.user_type != 'admin':
        return redirect('login')
    
    customers = account_models.Customer.objects.all().order_by('-create_at')
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'admin_user': request.user,
        'customers': page_obj,
    }
    return render(request, 'admin/customers_list.html', context)

def customers_create(request):
    if request.method == 'POST':
        # Extracting data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')  
        status = request.POST.get('status')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        is_default = request.POST.get('is_default') == 'on'

        # Retrieve the profile image
        profile_image = request.FILES.get('profile')

        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('customers_create')

        try:
            with transaction.atomic():  # Use transaction for atomicity
                # Create a new user instance
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    user_type='customer',  # Set user type to customer
                    password=make_password(password)  # Hash the password
                )
                user.save()

                # Create a new customer instance
                customer = account_models.Customer(
                    user=user,
                    profile_image=profile_image,
                    phone_number=phone_number,
                    status=status,
                )
                customer.save()

                # Create a new address book entry
                address = account_models.AddressBook(
                    customer=customer,
                    address_line_1=address_line_1,
                    address_line_2=address_line_2,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    country=country,
                    is_default=is_default
                )
                address.save()

                # Add a success message
                messages.success(request, "Customer created successfully!")
                return redirect('customers_list')  # Redirect to the customer list or another page

        except Exception as e:
            messages.error(request, "An error occurred: {}".format(str(e)))
            return redirect('customers_create')

    # If GET request, render the form
    context = {
        'admin_user': request.admin_user,
    }
    return render(request, 'admin/customers_create.html', context)

def customers_edit(request, id):
    customer = get_object_or_404(account_models.Customer, id=id)
    user = customer.user
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')  
        status = request.POST.get('status')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        is_default = request.POST.get('is_default') == 'on'
        
        # Retrieve the profile image (if updated)
        profile_image = request.FILES.get('profile')

        # Basic password validation
        if password and password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('customers_edit', customer_id=id)

        try:
            with transaction.atomic():  # Use transaction for atomicity
                # Update user details
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                
                if password:  # Update password only if provided
                    user.password = make_password(password)

                user.save()

                # Update customer details
                customer.phone_number = phone_number
                customer.status = status

                if profile_image:
                    customer.profile_image = profile_image

                customer.save()

                # Update address book
                address, created = account_models.AddressBook.objects.get_or_create(customer=customer, is_default=True)
                address.address_line_1 = address_line_1
                address.address_line_2 = address_line_2
                address.city = city
                address.state = state
                address.postal_code = postal_code
                address.country = country
                address.is_default = is_default
                address.save()

                # Add a success message
                messages.success(request, "Customer details updated successfully!")
                return redirect('customers_list')

        except Exception as e:
            messages.error(request, "An error occurred: {}".format(str(e)))
            return redirect('customers_edit', customer_id=id)

    # If GET request, pre-fill form fields with existing data
    context = {
        'customer': customer,
        'user': user,  # Send user details to template for pre-filling form
        'address': account_models.AddressBook.objects.get(customer=customer, is_default=True)  # Fetch default address
    }
    return render(request, 'admin/customers_edit.html', context)

def customers_delete(request, id):
    if request.method == 'POST':
        if request.user.user_type != 'admin':
            return JsonResponse({'success': False, 'message': 'Unauthorized access.'}, status=403)
        customer = get_object_or_404(account_models.Customer, id=id)
        try:
            user = customer.user  # Get the associated User instance
            customer.delete()  # Delete the customer first
            # Now delete the user manually
            print(user)
            user.delete()
            return JsonResponse({'success': True, 'message': 'Deleted successfully!'})
        except Exception as e:
            logger.exception("An error occurred while deleting customer and user.")
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)



def banners_list(request):
    if not request.user.is_authenticated or request.user.user_type != 'admin':
        return redirect('login')

    banners = models.BannerSlider.objects.all().order_by('order')
    paginator = Paginator(banners, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'admin_user': request.user,
        'banners': page_obj,
    }
    return render(request, 'admin/banners_list.html', context)

def banner_create(request):
    if not request.admin_user:
        return redirect('login')
    if request.method == 'POST':
        # Get the form data
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        button_text = request.POST.get('button_text')
        button_link = request.POST.get('button_link')
        image = request.FILES.get('image')
        order = request.POST.get('order')
        is_active = request.POST.get('is_active') == 'on'  # checkbox returns 'on' if checked
        # Create the banner
        # banner_create only if 3 banner is active ( do latter ) 
        try:
            banner = models.BannerSlider.objects.create(
                title=title,
                subtitle=subtitle,
                button_text=button_text,
                button_link=button_link,
                image=image,
                order=order,
                is_active=is_active
            )
            messages.success(request, 'Banner created successfully!')
            return redirect('banners_list')
        except Exception as e:
            messages.error(request, f'Error creating banner: {str(e)}')
    context = {
        'admin_user': request.admin_user,
    }
    return render(request, 'admin/banner_create.html', context)

def banner_edit(request, id):
    if not request.admin_user:
        return redirect('login')
    banner = get_object_or_404(models.BannerSlider, id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        button_text = request.POST.get('button_text')
        button_link = request.POST.get('button_link')
        image = request.FILES.get('image')
        order = request.POST.get('order')
        is_active = request.POST.get('is_active') == 'on'
        # Update the banner
        try:
            banner.title = title
            banner.subtitle = subtitle
            banner.button_text = button_text
            banner.button_link = button_link
            if image:  # Only update the image if a new one is provided
                banner.image = image
            banner.order = order
            banner.is_active = is_active
            banner.save()
            
            messages.success(request, 'Banner updated successfully!')
            return redirect('banners_list')
        except Exception as e:
            messages.error(request, f'Error updating banner: {str(e)}')

    context = {
        'admin_user': request.admin_user,
        'banner': banner,
    }
    return render(request, 'admin/banner_edit.html', context)

def banner_delete(request, id):
    if request.method == 'POST':
        if not request.admin_user:
            return JsonResponse({'success': False, 'message': 'Unauthorized access.'}, status=403)
        banner = get_object_or_404(models.BannerSlider, id=id)
        try:
            banner.delete()
            messages.success(request, 'Banner deleted successfully!')
            return JsonResponse({'success': True, 'message': 'Deleted successfully!'})
        except Exception as e:
            logger.exception("An error occurred while deleting the banner.")
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

