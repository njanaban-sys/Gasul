from django.urls import path
from django.shortcuts import redirect

# Mounted at '' in root urls.py so that visiting / redirects cleanly
urlpatterns = [
    path('', lambda request: redirect('products:home'), name='root'),
]
