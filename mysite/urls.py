from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from elevix.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("elevix/", include("elevix.urls")),
    path('', index, name='index'),

]

if settings.DEBUG:  # только в режиме разработки
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    # 🔥 ДОДАЙТЕ ЦЕ - для показу медіа-файлів у розробці
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
