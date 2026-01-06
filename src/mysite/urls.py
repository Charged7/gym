from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from elevix.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("elevix/", include("elevix.urls")),
    path('', index, name='index'),

]

# только в режиме разработки
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
