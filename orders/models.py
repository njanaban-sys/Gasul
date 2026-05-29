import uuid
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class CartItem(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1)
    added_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} – {self.product.name}'

    @property
    def subtotal(self):
        return self.product.discounted_price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('cod',   'Cash on Delivery'),
        ('gcash', 'GCash'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid',    'Paid'),
    ]

    id                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user                 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount         = models.DecimalField(max_digits=12, decimal_places=2)
    status               = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method       = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')
    gcash_reference      = models.CharField(max_length=100, blank=True, default='')
    is_paid              = models.BooleanField(default=False)
    delivery_address     = models.TextField()
    special_instructions = models.TextField(blank=True, default='')
    admin_notes          = models.TextField(blank=True, default='')
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.short_id} – {self.user.username} – {self.status}'

    @property
    def short_id(self):
        return str(self.id)[:8].upper()

    @property
    def payment_method_display(self):
        return dict(self.PAYMENT_CHOICES).get(self.payment_method, self.payment_method)

    @property
    def payment_status_display(self):
        return 'Paid' if self.is_paid else 'Pending'


class PaymentStatusLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    previous_status = models.CharField(max_length=10, choices=Order.PAYMENT_STATUS_CHOICES)
    updated_status = models.CharField(max_length=10, choices=Order.PAYMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.order.short_id}: {self.previous_status} → {self.updated_status} by {self.user.username if self.user else "System"} on {self.created_at:%Y-%m-%d %H:%M}'


class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity   = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} ×{self.quantity}'

    @property
    def subtotal(self):
        return self.unit_price * self.quantity
