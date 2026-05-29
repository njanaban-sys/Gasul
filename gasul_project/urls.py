from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),

    # Each app owns its own URL namespace
    path('users/',     include('users.urls',     namespace='users')),
    path('products/',  include('products.urls',  namespace='products')),
    path('orders/',    include('orders.urls',    namespace='orders')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),

    # Root redirect — login/home handled by users app
    path('', include('users.urls_root')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
