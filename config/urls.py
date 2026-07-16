from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap
from core.views import custom_404

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Assign the custom 404 handler
handler404 = 'core.views.custom_404'

# Catch-all pattern to catch all invalid URLs before CommonMiddleware redirects them
from django.urls import re_path
from core.views import custom_404
urlpatterns += [
    re_path(r'^.*$', custom_404),
]
