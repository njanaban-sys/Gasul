from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/',                    views.cart,             name='cart'),
    path('cart/add/<int:pk>/',       views.add_to_cart,      name='add_to_cart'),
    path('cart/update/<int:pk>/',    views.update_cart,      name='update_cart'),
    path('cart/remove/<int:pk>/',    views.remove_from_cart, name='remove_from_cart'),
    path('checkout/',                views.checkout,         name='checkout'),
    path('checkout/place/',          views.place_order,      name='place_order'),
    path('history/',                 views.order_list,       name='list'),
    path('history/<uuid:pk>/',       views.order_detail,     name='detail'),
]
