from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Product, Category, WishlistItem, Feedback
from users.decorators import regular_user_required


def home(request):
    category_slug = request.GET.get('category', '')
    search        = request.GET.get('search', '')
    products      = Product.objects.filter(is_active=True).select_related('category')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    categories        = Category.objects.all()
    selected_category = Category.objects.filter(slug=category_slug).first() if category_slug else None

    return render(request, 'products/home.html', {
        'products':          products,
        'categories':        categories,
        'selected_category': selected_category,
        'search':            search,
    })


def product_detail(request, pk):
    product     = get_object_or_404(Product, pk=pk, is_active=True)
    in_wishlist = False
    if request.user.is_authenticated and not (request.user.is_staff or request.user.is_superuser):
        in_wishlist = WishlistItem.objects.filter(user=request.user, product=product).exists()
    return render(request, 'products/product_detail.html', {
        'product':     product,
        'in_wishlist': in_wishlist,
    })


# ── Wishlist ──────────────────────────────────────────────────────

@regular_user_required
def wishlist(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product__category')
    return render(request, 'products/wishlist.html', {'items': items})


@regular_user_required
def toggle_wishlist(request, pk):
    product     = get_object_or_404(Product, pk=pk)
    item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()
        messages.info(request, f'"{product.name}" removed from wishlist.')
    else:
        messages.success(request, f'"{product.name}" added to wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'products:wishlist'))


# ── Feedback ──────────────────────────────────────────────────────

def feedback(request):
    published = Feedback.objects.filter(is_published=True)
    if request.method == 'POST':
        name         = request.POST.get('name', '').strip()
        email        = request.POST.get('email', '').strip()
        rating       = request.POST.get('rating', 5)
        message_text = request.POST.get('message', '').strip()
        if not name or not message_text:
            messages.error(request, 'Name and message are required.')
        else:
            Feedback.objects.create(
                user    = request.user if request.user.is_authenticated else None,
                name    = name,
                email   = email,
                rating  = rating,
                message = message_text,
            )
            messages.success(request, 'Thank you for your feedback!')
            return redirect('products:feedback')
    return render(request, 'products/feedback.html', {'feedbacks': published})
