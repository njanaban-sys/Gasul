from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',                          views.home,           name='home'),
    path('orders/',                   views.orders,         name='orders'),
    path('orders/<uuid:pk>/',         views.order_detail,   name='order_detail'),
    path('products/',                 views.products,       name='products'),
    path('products/add/',             views.product_edit,   name='product_add'),
    path('products/<int:pk>/edit/',   views.product_edit,   name='product_edit'),
    path('products/<int:pk>/toggle/', views.product_toggle, name='product_toggle'),
    path('users/',                    views.users,          name='users'),
    path('carts/',                    views.carts,          name='carts'),
    path('feedback/',                 views.feedback,       name='feedback'),
    path('categories/',               views.categories,     name='categories'),
]
