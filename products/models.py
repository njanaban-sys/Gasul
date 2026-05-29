from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Category(models.Model):
    name        = models.CharField(max_length=80, unique=True)
    slug        = models.SlugField(max_length=80, unique=True)
    description = models.TextField(blank=True, default='')
    icon        = models.CharField(max_length=10, default='🔥')
    order       = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name             = models.CharField(max_length=150)
    description      = models.TextField(blank=True, default='')
    price            = models.DecimalField(max_digits=10, decimal_places=2,
                           validators=[MinValueValidator(0)])
    stock            = models.PositiveIntegerField(default=0)
    image            = models.ImageField(upload_to='products/', blank=True, null=True)
    # One FK = one category per product — DB-enforced
    category         = models.ForeignKey(Category, on_delete=models.PROTECT,
                           related_name='products')
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                           validators=[MinValueValidator(0)])
    is_active        = models.BooleanField(default=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        if self.discount_percent:
            from decimal import Decimal
            return self.price * (1 - self.discount_percent / 100)
        return self.price

    @property
    def is_available(self):
        return self.is_active and self.stock > 0


class WishlistItem(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} ♡ {self.product.name}'


class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user         = models.ForeignKey(User, on_delete=models.SET_NULL,
                       null=True, blank=True)
    name         = models.CharField(max_length=100)
    email        = models.EmailField(blank=True, default='')
    rating       = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    message      = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} – {self.rating}★'
