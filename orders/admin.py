from django.contrib import admin
from .models import CartItem, Order, OrderItem, PaymentStatusLog


class OrderItemInline(admin.TabularInline):
    model         = OrderItem
    extra         = 0
    readonly_fields = ['product', 'quantity', 'unit_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display   = ['short_id', 'user', 'total_amount', 'payment_method', 'is_paid', 'status', 'created_at']
    list_filter    = ['status', 'payment_method', 'is_paid']
    list_editable  = ['status']
    search_fields  = ['user__username', 'delivery_address']
    inlines        = [OrderItemInline]
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(PaymentStatusLog)
class PaymentStatusLogAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'previous_status', 'updated_status', 'created_at']
    list_filter = ['previous_status', 'updated_status', 'created_at']
    search_fields = ['order__user__username', 'order__id', 'user__username']
    readonly_fields = ['order', 'user', 'previous_status', 'updated_status', 'created_at']

admin.site.register(CartItem)
