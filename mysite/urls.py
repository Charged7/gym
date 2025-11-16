from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("elevix/", include("elevix.urls")),
]

if settings.DEBUG:  # только в режиме разработки
    # For blog
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #----------------------

    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
