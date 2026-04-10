from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import health_check, serve_static_asset

admin.site.site_header = "Brazilian Sushi Admin"
admin.site.site_title = "Brazilian Sushi Admin"
admin.site.index_title = "Operations Dashboard"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("static/<path:path>", serve_static_asset, name="static-asset"),
    path("api/health/", health_check, name="api-health"),
    path("api/accounts/", include("accounts.urls")),
    path("api/menu/", include("menu.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/marketing/", include("marketing.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
