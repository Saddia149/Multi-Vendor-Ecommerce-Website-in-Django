from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Category, CustomUser
from .forms import ProductForm

# ✅ Buyer Homepage (Shows Trending Products)
def home(request):
    trending_products = Product.objects.filter(trending=True, status=True)  # Public trending products
    return render(request, "store/index.html", {'trending_products': trending_products})

# ✅ Buyer Collections View
def collections(request):
    category = Category.objects.filter(status=0)  # Show active categories
    return render(request, "store/collections.html", {'category': category})

# ✅ Buyer Collection Products View (Only Public Products)
def collectionsview(request, slug):
    category = get_object_or_404(Category, slug=slug, status=0)
    products = Product.objects.filter(category=category, status=True)
    return render(request, 'store/products/index.html', {'products': products, 'category': category})

# ✅ Buyer Product Detail View
# ✅ Buyer Product Detail View
def productview(request, cate_slug, prod_slug):
    category = get_object_or_404(Category, slug=cate_slug)
    product = get_object_or_404(Product, category=category, slug=prod_slug, status=True)

    return render(request, 'store/products/view.html', {
        'product': product,
        'category': category
    })

def product_autocomplete(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(name__icontains=request.GET.get('term'))
        results = []
        for product in qs:
            results.append({
                'label': product.name,
                'value': product.name,
                'url': product.get_absolute_url()  # assumes you’ve defined this method
            })
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

def productlistAjax(request):
    # Get all product names for the autocomplete dropdown
    products = Product.objects.filter(status=True).values_list('name', flat=True)
    product_names = list(products)
    return JsonResponse(product_names, safe=False)


# ✅ Product Search for Buyers
def search_product(request):
    query = request.GET.get('term')
    try:
        product = Product.objects.get(name__iexact=query)
        return redirect(product.get_absolute_url())
    except Product.DoesNotExist:
        return redirect("/")  # or render a 'no result found' page




# ✅ Seller Dashboard - Manages Their Own Products
@login_required(login_url='loginpage')
def seller_dashboard(request):
    if request.user.role != 'seller':
        return redirect('/')  # ✅ Restrict access to sellers only
    
    products = Product.objects.filter(seller=request.user)  # ✅ Ensure correct filtering

    return render(request, 'store/seller_dashboard.html', {'products': products})



# ✅ Seller Adds a New Product
@login_required(login_url='loginpage')
def add_product(request):
    if request.user.role != 'seller':
        return redirect('/')

    form = ProductForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.status = True  # 🔴 Force product to be visible
            product.save()
            return redirect('seller_dashboard')
    return render(request, 'store/add_product.html', {'form': form})

@login_required(login_url='loginpage')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)  # ✅ Ensure correct seller filtering

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST":
        if form.is_valid():
            product = form.save(commit=False)  # ✅ Prevent overwriting seller field
            product.seller = request.user  # ✅ Explicitly reassign seller before saving
            product.save()
            return redirect('/seller-dashboard/')  # ✅ Redirect after successful update
        else:
            print(form.errors)  # ✅ Debug errors

    return render(request, "store/edit_product.html", {'form': form, 'product': product})



# ✅ Seller Deletes Their Own Product
@login_required(login_url='loginpage')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)  
    product.delete()
    return redirect('seller_dashboard')
