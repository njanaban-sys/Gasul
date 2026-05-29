from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('',                           views.home,           name='home'),
    path('<int:pk>/',                  views.product_detail, name='detail'),
    path('wishlist/',                  views.wishlist,       name='wishlist'),
    path('wishlist/toggle/<int:pk>/',  views.toggle_wishlist, name='toggle_wishlist'),
    path('feedback/',                  views.feedback,       name='feedback'),
]
