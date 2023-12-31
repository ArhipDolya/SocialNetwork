from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="MovieFusion API",
        default_version='v1',
        description="API for MovieFusion project",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="MovieFusionLicence"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('user_auth.urls')),
    path('api/v1/', include('posts.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("__debug__/", include("debug_toolbar.urls")),
]
