from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from myadmin import models

User = get_user_model()  # Get the custom user model

def admin_dashboard(request):
    # Check if the user session exists (handled by middleware)
    if not request.admin_user:
        return redirect('login')

    context = {
        'admin_user': request.admin_user,
    }
    return render(request, 'admin/dashboard.html',context)


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
