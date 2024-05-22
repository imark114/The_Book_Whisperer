from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account import urls as accounts_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(accounts_urls)),
    path('book/', include('book.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)