from django.contrib import admin
from .models import Category, Product, WishlistItem, Feedback


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display   = ['name', 'slug', 'icon', 'order']
    list_editable  = ['order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category', 'price', 'discount_percent', 'stock', 'is_active']
    list_editable = ['price', 'stock', 'discount_percent', 'is_active']
    list_filter   = ['category', 'is_active']
    search_fields = ['name']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display  = ['name', 'rating', 'is_published', 'created_at']
    list_editable = ['is_published']
    list_filter   = ['rating', 'is_published']


admin.site.register(WishlistItem)
