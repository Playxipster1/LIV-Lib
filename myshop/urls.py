from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]

# АВТОМАТИЧЕСКАЯ обработка статических файлов в разработке
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработчики ошибок
handler404 = 'products.views.custom_404'
handler500 = 'products.views.custom_500'
handler403 = 'products.views.custom_403'
handler400 = 'products.views.custom_400'