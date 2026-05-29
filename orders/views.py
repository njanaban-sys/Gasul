from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from decimal import Decimal

from products.models import Product
from .models import CartItem, Order, OrderItem
from users.decorators import regular_user_required


# ── Cart ──────────────────────────────────────────────────────────

@regular_user_required
def cart(request):
    items = CartItem.objects.filter(user=request.user).select_related('product__category')
    total = sum(item.subtotal for item in items)
    return render(request, 'orders/cart.html', {'items': items, 'total': total})


@regular_user_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    qty     = max(1, int(request.POST.get('quantity', 1)))

    if product.stock < qty:
        messages.error(request, f'Only {product.stock} unit(s) in stock.')
        return redirect('products:detail', pk=pk)

    item, created = CartItem.objects.get_or_create(
        user=request.user, product=product, defaults={'quantity': 0}
    )
    new_qty = item.quantity + qty
    if product.stock < new_qty:
        messages.error(request, f'Cannot add {qty} more. Only {product.stock - item.quantity} left.')
        return redirect('orders:cart')

    item.quantity = new_qty
    item.save()
    messages.success(request, f'"{product.name}" added to cart.')
    return redirect('orders:cart')


@regular_user_required
def update_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    qty  = int(request.POST.get('quantity', 1))
    if qty <= 0:
        item.delete()
        messages.success(request, 'Item removed from cart.')
    elif item.product.stock < qty:
        messages.error(request, f'Only {item.product.stock} unit(s) available.')
    else:
        item.quantity = qty
        item.save()
    return redirect('orders:cart')


@regular_user_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('orders:cart')


# ── Checkout ──────────────────────────────────────────────────────

@regular_user_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user).select_related('product__category')
    if not items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('orders:cart')
    total = sum(item.subtotal for item in items)
    return render(request, 'orders/checkout.html', {'items': items, 'total': total})


@regular_user_required
@transaction.atomic
def place_order(request):
    if request.method != 'POST':
        return redirect('orders:checkout')

    items = list(CartItem.objects.filter(user=request.user).select_related('product'))
    if not items:
        messages.error(request, 'Your cart is empty.')
        return redirect('orders:cart')

    # Stock validation
    for item in items:
        if item.product.stock < item.quantity:
            messages.error(request, f'"{item.product.name}" only has {item.product.stock} unit(s) left.')
            return redirect('orders:cart')

    delivery_address     = request.POST.get('delivery_address', '').strip()
    special_instructions = request.POST.get('special_instructions', '').strip()
    payment_method       = request.POST.get('payment_method', 'cod')
    gcash_reference      = request.POST.get('gcash_reference', '').strip()

    if not delivery_address:
        messages.error(request, 'Delivery address is required.')
        return redirect('orders:checkout')
    if payment_method not in ('cod', 'gcash'):
        messages.error(request, 'Please select a valid payment method.')
        return redirect('orders:checkout')
    if payment_method == 'gcash' and not gcash_reference:
        messages.error(request, 'GCash reference number is required.')
        return redirect('orders:checkout')

    total = sum(item.subtotal for item in items)

    order = Order.objects.create(
        user                 = request.user,
        total_amount         = total,
        status               = 'pending',
        payment_method       = payment_method,
        gcash_reference      = gcash_reference,
        is_paid              = (payment_method == 'gcash'),
        delivery_address     = delivery_address,
        special_instructions = special_instructions,
    )

    for item in items:
        OrderItem.objects.create(
            order      = order,
            product    = item.product,
            quantity   = item.quantity,
            unit_price = item.product.discounted_price,
        )
        item.product.stock -= item.quantity
        item.product.save()

    CartItem.objects.filter(user=request.user).delete()
    messages.success(request, f'Order #{order.short_id} placed successfully!')
    return redirect('orders:detail', pk=order.pk)


# ── Order history ─────────────────────────────────────────────────

@regular_user_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/order_list.html', {'orders': orders})


@regular_user_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
