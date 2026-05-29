from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q, Prefetch
from decimal import Decimal

from products.models import Category, Product, Feedback
from orders.models import CartItem, Order, OrderItem, PaymentStatusLog
from users.decorators import admin_required


@admin_required
def home(request):
    total_orders   = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_revenue  = Order.objects.filter(
        status__in=['confirmed', 'processing', 'shipped', 'delivered']
    ).aggregate(rev=Sum('total_amount'))['rev'] or 0
    total_products  = Product.objects.filter(is_active=True).count()
    low_stock       = Product.objects.filter(stock__lte=5, is_active=True).count()
    recent_orders   = Order.objects.select_related('user').prefetch_related('items')[:10]
    total_users     = User.objects.filter(is_staff=False, is_superuser=False).count()
    pending_feedback = Feedback.objects.filter(is_published=False).count()

    return render(request, 'dashboard/home.html', {
        'total_orders':     total_orders,
        'pending_orders':   pending_orders,
        'total_revenue':    total_revenue,
        'total_products':   total_products,
        'low_stock':        low_stock,
        'recent_orders':    recent_orders,
        'total_users':      total_users,
        'pending_feedback': pending_feedback,
    })


# ── Orders ────────────────────────────────────────────────────────

@admin_required
def orders(request):
    status_filter       = request.GET.get('status', '')
    payment_filter      = request.GET.get('payment', '')
    payment_status_filter = request.GET.get('payment_status', '')
    search              = request.GET.get('search', '')

    qs = Order.objects.select_related('user').prefetch_related('items__product')
    if status_filter:
        qs = qs.filter(status=status_filter)
    if payment_filter:
        qs = qs.filter(payment_method=payment_filter)
    if payment_status_filter in dict(Order.PAYMENT_STATUS_CHOICES):
        qs = qs.filter(is_paid=(payment_status_filter == 'paid'))
    if search:
        qs = qs.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(delivery_address__icontains=search)
        )

    return render(request, 'dashboard/orders.html', {
        'orders':               qs,
        'status_choices':       Order.STATUS_CHOICES,
        'payment_choices':      Order.PAYMENT_CHOICES,
        'payment_status_choices': Order.PAYMENT_STATUS_CHOICES,
        'status_filter':        status_filter,
        'payment_filter':       payment_filter,
        'payment_status_filter': payment_status_filter,
        'search':               search,
    })


@admin_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status      = request.POST.get('status')
        new_payment_status = request.POST.get('payment_status')
        admin_notes     = request.POST.get('admin_notes', '').strip()
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
        if new_payment_status in dict(Order.PAYMENT_STATUS_CHOICES):
            previous_payment_status = 'paid' if order.is_paid else 'pending'
            if new_payment_status != previous_payment_status:
                order.is_paid = (new_payment_status == 'paid')
                PaymentStatusLog.objects.create(
                    order=order,
                    user=request.user,
                    previous_status=previous_payment_status,
                    updated_status=new_payment_status,
                )
        order.admin_notes = admin_notes
        order.save()
        messages.success(request, f'Order #{order.short_id} updated.')
        return redirect('dashboard:order_detail', pk=pk)

    payment_logs = order.payment_logs.select_related('user').all()
    last_payment_date = payment_logs.first().created_at if payment_logs.exists() else order.created_at
    return render(request, 'dashboard/order_detail.html', {
        'order':                order,
        'status_choices':       Order.STATUS_CHOICES,
        'payment_status_choices': Order.PAYMENT_STATUS_CHOICES,
        'payment_logs':         payment_logs,
        'last_payment_date':    last_payment_date,
    })


# ── Products ──────────────────────────────────────────────────────

@admin_required
def products(request):
    search        = request.GET.get('search', '')
    category_slug = request.GET.get('category', '')
    qs            = Product.objects.select_related('category').all()
    if search:
        qs = qs.filter(name__icontains=search)
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    return render(request, 'dashboard/products.html', {
        'products':     qs,
        'categories':   Category.objects.all(),
        'search':       search,
        'category_slug': category_slug,
    })


@admin_required
def product_edit(request, pk=None):
    product    = get_object_or_404(Product, pk=pk) if pk else None
    categories = Category.objects.all()

    if request.method == 'POST':
        name             = request.POST.get('name', '').strip()
        description      = request.POST.get('description', '').strip()
        price            = request.POST.get('price', '0')
        stock            = request.POST.get('stock', '0')
        category_id      = request.POST.get('category')
        discount_percent = request.POST.get('discount_percent', '0')
        is_active        = request.POST.get('is_active') == 'on'

        if not name or not category_id:
            messages.error(request, 'Name and category are required.')
        else:
            category = get_object_or_404(Category, pk=category_id)
            if product is None:
                product = Product(category=category)
            else:
                product.category = category
            product.name             = name
            product.description      = description
            product.price            = Decimal(price)
            product.stock            = int(stock)
            product.discount_percent = Decimal(discount_percent)
            product.is_active        = is_active
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            product.save()
            messages.success(request, f'Product "{product.name}" saved.')
            return redirect('dashboard:products')

    return render(request, 'dashboard/product_edit.html', {
        'product':    product,
        'categories': categories,
    })


@admin_required
def product_toggle(request, pk):
    product          = get_object_or_404(Product, pk=pk)
    product.is_active = not product.is_active
    product.save()
    state = 'activated' if product.is_active else 'deactivated'
    messages.success(request, f'"{product.name}" {state}.')
    return redirect('dashboard:products')


# ── Users ─────────────────────────────────────────────────────────

@admin_required
def users(request):
    qs = User.objects.filter(
        is_staff=False, is_superuser=False
    ).annotate(order_count=Count('orders')).order_by('-date_joined')
    return render(request, 'dashboard/users.html', {'users': qs})


# ── Carts ─────────────────────────────────────────────────────────

@admin_required
def carts(request):
    users_with_carts = User.objects.filter(
        cart_items__isnull=False
    ).distinct().prefetch_related(
        Prefetch('cart_items', queryset=CartItem.objects.select_related('product'))
    )
    return render(request, 'dashboard/carts.html', {'users_with_carts': users_with_carts})


# ── Feedback ──────────────────────────────────────────────────────

@admin_required
def feedback(request):
    feedbacks = Feedback.objects.all()
    if request.method == 'POST':
        fid    = request.POST.get('feedback_id')
        action = request.POST.get('action')
        fb     = get_object_or_404(Feedback, pk=fid)
        if action == 'publish':
            fb.is_published = True; fb.save()
            messages.success(request, 'Feedback published.')
        elif action == 'unpublish':
            fb.is_published = False; fb.save()
            messages.success(request, 'Feedback unpublished.')
        elif action == 'delete':
            fb.delete()
            messages.success(request, 'Feedback deleted.')
        return redirect('dashboard:feedback')
    return render(request, 'dashboard/feedback.html', {'feedbacks': feedbacks})


# ── Categories ────────────────────────────────────────────────────

@admin_required
def categories(request):
    cats = Category.objects.annotate(product_count=Count('products'))
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            name        = request.POST.get('name', '').strip()
            slug        = request.POST.get('slug', '').strip()
            icon        = request.POST.get('icon', '🔥').strip()
            description = request.POST.get('description', '').strip()
            if name and slug:
                Category.objects.get_or_create(slug=slug, defaults={
                    'name': name, 'icon': icon, 'description': description
                })
                messages.success(request, f'Category "{name}" added.')
            else:
                messages.error(request, 'Name and slug are required.')
        elif action == 'delete':
            cat = get_object_or_404(Category, pk=request.POST.get('category_id'))
            if cat.products.exists():
                messages.error(request, f'Cannot delete "{cat.name}" — it has products.')
            else:
                cat.delete()
                messages.success(request, 'Category deleted.')
        return redirect('dashboard:categories')
    return render(request, 'dashboard/categories.html', {'categories': cats})
